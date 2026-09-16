"""Folder/VOC image discovery, deterministic splitting, and DataLoaders."""
from __future__ import annotations

import random
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

import torch
from PIL import Image
from torch.utils.data import DataLoader, Dataset
from torchvision import transforms

from .config import Config


class ImageSubset(Dataset):
    def __init__(self, samples: list[tuple[Path, tuple[float, float, float, float], int]], indices: list[int], transform: Any) -> None:
        self.samples = samples
        self.indices = indices
        self.transform = transform

    def __len__(self) -> int:
        return len(self.indices)

    def __getitem__(self, position: int) -> tuple[torch.Tensor, int]:
        image_path, box, label = self.samples[self.indices[position]]
        with Image.open(image_path) as opened:
            image = opened.convert("RGB").crop(box)
        return self.transform(image), label


def _split_class_indices(targets: list[int], config: Config) -> tuple[list[int], list[int], list[int]]:
    rng = random.Random(config.seed)
    train, validation, test = [], [], []
    for label in sorted(set(targets)):
        indices = [index for index, target in enumerate(targets) if target == label]
        rng.shuffle(indices)
        count = len(indices)
        if count < 3:
            raise ValueError(f"Class {label} has {count} image(s); at least 3 are required for three splits")
        test_count = max(1, round(count * config.test_fraction))
        validation_count = max(1, round(count * config.validation_fraction))
        if test_count + validation_count >= count:
            validation_count = 1
            test_count = 1
        test.extend(indices[:test_count])
        validation.extend(indices[test_count:test_count + validation_count])
        train.extend(indices[test_count + validation_count:])
    rng.shuffle(train)
    rng.shuffle(validation)
    rng.shuffle(test)
    return train, validation, test


def build_transforms(config: Config, extra_augmentation: bool = False) -> tuple[Any, Any]:
    normalization = transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    train_steps = [transforms.Resize((config.image_size, config.image_size))]
    if extra_augmentation:
        train_steps.append(transforms.RandomResizedCrop(config.image_size, scale=(0.8, 1.0)))
    train_steps.extend([
        transforms.RandomHorizontalFlip(),
        transforms.RandomRotation(8),
        transforms.ToTensor(),
        normalization,
    ])
    train_transform = transforms.Compose(train_steps)
    evaluation_transform = transforms.Compose([
        transforms.Resize((config.image_size, config.image_size)),
        transforms.ToTensor(),
        normalization,
    ])
    return train_transform, evaluation_transform


def _voc_samples(dataset_path: Path) -> tuple[list[tuple[Path, tuple[float, float, float, float], int]], list[str], list[str]]:
    xml_files = sorted(dataset_path.rglob("*.xml"))
    if not xml_files:
        raise ValueError(f"No Pascal VOC XML annotations found below {dataset_path}")
    image_paths = {path.name: path for path in dataset_path.rglob("*.jpg")}
    class_names = sorted({obj.findtext("name", "").strip() for xml_file in xml_files for obj in ET.parse(xml_file).getroot().findall("object") if obj.findtext("name", "").strip()})
    class_to_index = {name: index for index, name in enumerate(class_names)}
    samples = []
    image_keys = []
    for xml_file in xml_files:
        root = ET.parse(xml_file).getroot()
        image_name = root.findtext("filename", xml_file.stem + ".jpg")
        image_path = image_paths.get(image_name, dataset_path / image_name)
        if not image_path.exists():
            raise FileNotFoundError(f"Annotation references missing image: {image_name}")
        image_keys.append(str(image_path))
        for obj in root.findall("object"):
            label_name = obj.findtext("name", "").strip()
            box = obj.find("bndbox")
            if not label_name or box is None:
                continue
            coordinates = tuple(float(box.findtext(field, "0")) for field in ("xmin", "ymin", "xmax", "ymax"))
            if coordinates[2] <= coordinates[0] or coordinates[3] <= coordinates[1]:
                raise ValueError(f"Invalid bounding box in {xml_file.name}")
            samples.append((image_path, coordinates, class_to_index[label_name]))
    return samples, class_names, image_keys


def _split_image_groups(samples: list[tuple[Path, tuple[float, float, float, float], int]], config: Config) -> tuple[list[int], list[int], list[int]]:
    rng = random.Random(config.seed)
    image_to_indices: dict[Path, list[int]] = {}
    for index, (image_path, _, _) in enumerate(samples):
        image_to_indices.setdefault(image_path, []).append(index)
    image_paths = list(image_to_indices)
    rng.shuffle(image_paths)
    test_count = max(1, round(len(image_paths) * config.test_fraction))
    validation_count = max(1, round(len(image_paths) * config.validation_fraction))
    if test_count + validation_count >= len(image_paths):
        raise ValueError("Not enough source images for train/validation/test splits")
    test_images = set(image_paths[:test_count])
    validation_images = set(image_paths[test_count:test_count + validation_count])
    train_images = set(image_paths[test_count + validation_count:])
    groups = [train_images, validation_images, test_images]
    result = [[index for image_path, indices in image_to_indices.items() if image_path in group for index in indices] for group in groups]
    if not all(result):
        raise ValueError("A train, validation, or test split has no labeled objects")
    return tuple(result)  # type: ignore[return-value]


def create_dataloaders(config: Config) -> tuple[dict[str, DataLoader], list[str], dict[str, int]]:
    config.validate()
    dataset_path = Path(config.dataset_path)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Image dataset directory does not exist: {dataset_path}")
    samples, classes, _ = _voc_samples(dataset_path)
    if len(samples) == 0:
        raise ValueError(f"No labeled objects found below {dataset_path}")
    train_indices, validation_indices, test_indices = _split_image_groups(samples, config)
    train_transform, evaluation_transform = build_transforms(config)
    subsets = {
        "train": ImageSubset(samples, train_indices, train_transform),
        "validation": ImageSubset(samples, validation_indices, evaluation_transform),
        "test": ImageSubset(samples, test_indices, evaluation_transform),
    }
    loaders = {
        name: DataLoader(
            subset,
            batch_size=config.batch_size,
            shuffle=name == "train",
            num_workers=config.num_workers,
            pin_memory=torch.cuda.is_available(),
        )
        for name, subset in subsets.items()
    }
    return loaders, classes, {name: len(subset) for name, subset in subsets.items()}
