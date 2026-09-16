"""Evaluation helpers and CLI for a trained baseline checkpoint."""
from __future__ import annotations

import argparse
from pathlib import Path

import torch
import torch.nn as nn

from .config import Config
from .dataset import create_dataloaders
from .metrics import classification_metrics, save_metrics
from .model import SimpleCNN


def evaluate_model(model: nn.Module, loader, device: torch.device) -> dict:
    model.eval()
    labels, predictions = [], []
    with torch.no_grad():
        for images, targets in loader:
            outputs = model(images.to(device))
            predictions.extend(outputs.argmax(dim=1).cpu().tolist())
            labels.extend(targets.tolist())
    return classification_metrics(labels, predictions, model.classifier[-1].out_features)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="data/raw/vehicle_images")
    parser.add_argument("--checkpoint", default="outputs/ml/baseline/best_model.pth")
    parser.add_argument("--output", default="outputs/ml/baseline/test_metrics.json")
    args = parser.parse_args()
    config = Config(dataset_path=Path(args.dataset), output_path=Path(args.output).parent)
    loaders, classes, sizes = create_dataloaders(config)
    checkpoint = torch.load(args.checkpoint, map_location="cpu")
    model = SimpleCNN(len(classes))
    model.load_state_dict(checkpoint["model_state_dict"])
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    metrics = evaluate_model(model.to(device), loaders["test"], device)
    metrics["classes"] = classes
    metrics["dataset_sizes"] = sizes
    save_metrics(metrics, Path(args.output))
    print(metrics)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
