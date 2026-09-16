"""Train and evaluate the reproducible baseline CNN."""
from __future__ import annotations

import argparse
import csv
import json
import random
import time
from pathlib import Path

import numpy as np
import torch
import torch.nn as nn
from torch.optim import Adam

from .config import Config
from .dataset import create_dataloaders
from .evaluate import evaluate_model
from .metrics import save_classification_report, save_confusion_matrix_png
from .model import SimpleCNN


def set_seed(seed: int) -> None:
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False


def run_epoch(model, loader, loss_function, optimizer, device, training: bool) -> tuple[float, float]:
    model.train(training)
    total_loss, correct, count = 0.0, 0, 0
    for images, targets in loader:
        images, targets = images.to(device), targets.to(device)
        if training:
            optimizer.zero_grad(set_to_none=True)
        outputs = model(images)
        loss = loss_function(outputs, targets)
        if training:
            loss.backward()
            optimizer.step()
        total_loss += loss.item() * targets.size(0)
        correct += int((outputs.argmax(dim=1) == targets).sum().item())
        count += targets.size(0)
    return total_loss / count, correct / count


def write_history(history: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(history[0]))
        writer.writeheader()
        writer.writerows(history)


def train(config: Config) -> dict:
    config.validate()
    set_seed(config.seed)
    config.output_path.mkdir(parents=True, exist_ok=True)
    loaders, classes, dataset_sizes = create_dataloaders(config)
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleCNN(len(classes)).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=config.learning_rate)
    best_validation_loss = float("inf")
    best_epoch = 0
    epochs_without_improvement = 0
    history: list[dict] = []
    started = time.perf_counter()

    print(f"device: {device}")
    if device.type == "cuda":
        print(f"gpu: {torch.cuda.get_device_name(device)}")
    print(f"classes: {len(classes)}")
    print(f"dataset_sizes: {dataset_sizes}")
    print(f"batch_size: {config.batch_size}")
    print(f"epochs: {config.epochs}")

    for epoch in range(1, config.epochs + 1):
        train_loss, train_accuracy = run_epoch(model, loaders["train"], loss_function, optimizer, device, True)
        validation_loss, validation_accuracy = run_epoch(model, loaders["validation"], loss_function, optimizer, device, False)
        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "validation_loss": validation_loss,
            "validation_accuracy": validation_accuracy,
        }
        history.append(row)
        print(row)
        if validation_loss < best_validation_loss:
            best_validation_loss = validation_loss
            best_epoch = epoch
            epochs_without_improvement = 0
            torch.save({
                "model_state_dict": model.state_dict(),
                "classes": classes,
                "config": config.as_dict(),
                "best_epoch": best_epoch,
            }, config.output_path / "best_model.pth")
        else:
            epochs_without_improvement += 1
            if epochs_without_improvement >= config.patience:
                break

    training_seconds = time.perf_counter() - started
    write_history(history, config.output_path / "training_history.csv")
    checkpoint = torch.load(config.output_path / "best_model.pth", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    test_metrics = evaluate_model(model, loaders["test"], device)
    test_metrics["classes"] = classes
    test_metrics["dataset_sizes"] = dataset_sizes
    test_metrics["device"] = str(device)
    (config.output_path / "test_metrics.json").write_text(json.dumps(test_metrics, indent=2), encoding="utf-8")
    (config.output_path / "metrics.json").write_text(json.dumps(test_metrics, indent=2), encoding="utf-8")
    save_classification_report(test_metrics, classes, config.output_path / "classification_report.txt")
    save_confusion_matrix_png(test_metrics, classes, config.output_path / "confusion_matrix.png")
    metadata = {
        "config": config.as_dict(),
        "classes": classes,
        "dataset_sizes": dataset_sizes,
        "device": str(device),
        "gpu_name": torch.cuda.get_device_name(device) if device.type == "cuda" else None,
        "best_epoch": best_epoch,
        "epochs_completed": len(history),
        "training_seconds": training_seconds,
        "test_metrics": test_metrics,
    }
    (config.output_path / "run_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    return metadata


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="data/raw/vehicle_images")
    parser.add_argument("--output", default="outputs/ml/baseline")
    parser.add_argument("--epochs", type=int, default=20)
    parser.add_argument("--batch-size", type=int, default=32)
    parser.add_argument("--learning-rate", type=float, default=1e-3)
    args = parser.parse_args()
    config = Config(dataset_path=Path(args.dataset), output_path=Path(args.output), epochs=args.epochs, batch_size=args.batch_size, learning_rate=args.learning_rate)
    train(config)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
