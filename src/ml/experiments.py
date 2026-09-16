"""Sequential, same-split CNN ablation experiments."""
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
from torch.optim.lr_scheduler import ReduceLROnPlateau
from torch.utils.data import DataLoader

from .config import Config
from .dataset import ImageSubset, _split_image_groups, _voc_samples, build_transforms
from .metrics import classification_metrics
from .model import SimpleCNN
from .train import run_epoch, set_seed


EXPERIMENTS = [
    {"name": "baseline", "batch_size": 32, "extra_augmentation": False, "weight_decay": 0.0, "dropout": 0.0, "scheduler": False},
    {"name": "batch", "batch_size": 16, "extra_augmentation": False, "weight_decay": 0.0, "dropout": 0.0, "scheduler": False},
    {"name": "augmentation", "batch_size": 32, "extra_augmentation": True, "weight_decay": 0.0, "dropout": 0.0, "scheduler": False},
    {"name": "regularization", "batch_size": 32, "extra_augmentation": False, "weight_decay": 1e-4, "dropout": 0.0, "scheduler": False},
    {"name": "dropout", "batch_size": 32, "extra_augmentation": False, "weight_decay": 0.0, "dropout": 0.30, "scheduler": False},
    {"name": "lr_schedule", "batch_size": 32, "extra_augmentation": False, "weight_decay": 0.0, "dropout": 0.0, "scheduler": True},
    {"name": "optimized", "batch_size": 32, "extra_augmentation": True, "weight_decay": 1e-4, "dropout": 0.30, "scheduler": True},
]
RESULT_FIELDS = [
    "experiment", "status", "error", "configuration", "device", "gpu_name", "batch_size", "epochs",
    "training_time_seconds", "best_epoch", "best_validation_accuracy", "test_accuracy", "precision", "recall",
    "f1", "final_train_accuracy", "final_validation_accuracy", "train_validation_gap", "learning_rates",
]


def build_loaders(config: Config, samples, split_indices, extra_augmentation: bool, batch_size: int):
    train_indices, validation_indices, test_indices = split_indices
    train_transform, evaluation_transform = build_transforms(config, extra_augmentation=extra_augmentation)
    subsets = {
        "train": ImageSubset(samples, train_indices, train_transform),
        "validation": ImageSubset(samples, validation_indices, evaluation_transform),
        "test": ImageSubset(samples, test_indices, evaluation_transform),
    }
    return {
        name: DataLoader(
            subset,
            batch_size=batch_size,
            shuffle=name == "train",
            num_workers=config.num_workers,
            pin_memory=torch.cuda.is_available(),
        )
        for name, subset in subsets.items()
    }


def evaluate_predictions(model, loader, device, num_classes):
    model.eval()
    labels, predictions = [], []
    with torch.no_grad():
        for images, targets in loader:
            outputs = model(images.to(device))
            predictions.extend(outputs.argmax(dim=1).cpu().tolist())
            labels.extend(targets.tolist())
    return classification_metrics(labels, predictions, num_classes)


def write_history(history: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(history[0]))
        writer.writeheader()
        writer.writerows(history)


def run_experiment(config: Config, experiment: dict, samples, classes, split_indices, device: torch.device, output_dir: Path, max_epochs: int) -> dict:
    set_seed(config.seed)
    loaders = build_loaders(config, samples, split_indices, experiment["extra_augmentation"], experiment["batch_size"])
    model = SimpleCNN(len(classes), dropout=experiment["dropout"]).to(device)
    loss_function = nn.CrossEntropyLoss()
    optimizer = Adam(model.parameters(), lr=config.learning_rate, weight_decay=experiment["weight_decay"])
    scheduler = ReduceLROnPlateau(optimizer, mode="min", factor=0.5, patience=2) if experiment["scheduler"] else None
    best_validation_accuracy = -1.0
    best_validation_loss = float("inf")
    best_epoch = 0
    history = []
    started = time.perf_counter()
    for epoch in range(1, max_epochs + 1):
        train_loss, train_accuracy = run_epoch(model, loaders["train"], loss_function, optimizer, device, True)
        validation_loss, validation_accuracy = run_epoch(model, loaders["validation"], loss_function, optimizer, device, False)
        if scheduler is not None:
            scheduler.step(validation_loss)
        current_lr = optimizer.param_groups[0]["lr"]
        row = {
            "epoch": epoch,
            "train_loss": train_loss,
            "train_accuracy": train_accuracy,
            "validation_loss": validation_loss,
            "validation_accuracy": validation_accuracy,
            "learning_rate": current_lr,
        }
        history.append(row)
        if validation_accuracy > best_validation_accuracy or (validation_accuracy == best_validation_accuracy and validation_loss < best_validation_loss):
            best_validation_accuracy = validation_accuracy
            best_validation_loss = validation_loss
            best_epoch = epoch
            torch.save({"model_state_dict": model.state_dict(), "classes": classes, "experiment": experiment, "best_epoch": epoch}, output_dir / f"{experiment['name']}_best_model.pth")
        print(experiment["name"], row)
    training_seconds = time.perf_counter() - started
    checkpoint = torch.load(output_dir / f"{experiment['name']}_best_model.pth", map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    metrics = evaluate_predictions(model, loaders["test"], device, len(classes))
    final = history[-1]
    result = {
        "experiment": experiment["name"],
        "status": "completed",
        "error": "",
        "configuration": json.dumps(experiment, sort_keys=True),
        "device": str(device),
        "gpu_name": torch.cuda.get_device_name(device) if device.type == "cuda" else "",
        "batch_size": experiment["batch_size"],
        "epochs": len(history),
        "training_time_seconds": training_seconds,
        "best_epoch": best_epoch,
        "best_validation_accuracy": best_validation_accuracy,
        "test_accuracy": metrics["accuracy"],
        "precision": metrics["macro_precision"],
        "recall": metrics["macro_recall"],
        "f1": metrics["macro_f1"],
        "final_train_accuracy": final["train_accuracy"],
        "final_validation_accuracy": final["validation_accuracy"],
        "train_validation_gap": final["train_accuracy"] - final["validation_accuracy"],
        "learning_rates": json.dumps([row["learning_rate"] for row in history]),
    }
    experiment_dir = output_dir / experiment["name"]
    experiment_dir.mkdir(parents=True, exist_ok=True)
    write_history(history, experiment_dir / "training_history.csv")
    (experiment_dir / "metrics.json").write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    return result


def save_results(results: list[dict], path: Path) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=RESULT_FIELDS, extrasaction="ignore")
        writer.writeheader()
        writer.writerows(results)


def load_results(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_partial_report(results: list[dict], output_dir: Path, split_sizes: dict[str, int]) -> None:
    def value(row: dict, key: str) -> str:
        raw = row.get(key, "")
        return f"{float(raw):.6f}" if raw not in ("", None) else ""

    lines = [
        "# CNN Controlled Experiments",
        "",
        "Experiments use the same fixed source-image split.",
        f"Split object-crop sizes: train={split_sizes['train']}, validation={split_sizes['validation']}, test={split_sizes['test']}.",
        "",
        "| Experiment | Status | Training Time | Val Accuracy | Test Accuracy | F1 | Train-Val Gap |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        time_value = row.get("training_time_seconds", "")
        time_text = f"{float(time_value):.4f}s" if time_value not in ("", None) else ""
        lines.append(f"| {row['experiment']} | {row['status']} | {time_text} | {value(row, 'best_validation_accuracy')} | {value(row, 'test_accuracy')} | {value(row, 'f1')} | {value(row, 'train_validation_gap')} |")
    (output_dir / "experiment_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_report(results: list[dict], output_dir: Path, classes: list[str], split_sizes: dict[str, int]) -> None:
    numeric_fields = [
        "training_time_seconds",
        "best_validation_accuracy",
        "validation_accuracy",
        "test_accuracy",
        "precision",
        "recall",
        "f1",
        "final_train_accuracy",
        "final_validation_accuracy",
        "train_validation_gap",
    ]
    for row in results:
        for field in numeric_fields:
            if field in row and row[field] not in ("", None):
                try:
                    row[field] = float(row[field])
                except (ValueError, TypeError):
                    pass
        if "best_validation_accuracy" in row and "validation_accuracy" not in row:
            row["validation_accuracy"] = row["best_validation_accuracy"]
        elif "validation_accuracy" in row and "best_validation_accuracy" not in row:
            row["best_validation_accuracy"] = row["validation_accuracy"]

    successful = [row for row in results if row.get("status") == "completed"]
    if not successful:
        write_partial_report(results, output_dir, split_sizes)
        return
    baseline = next((row for row in successful if row["experiment"] == "baseline"), None)
    optimized = next((row for row in successful if row["experiment"] == "optimized"), None)
    best = max(successful, key=lambda row: float(row.get("best_validation_accuracy", row.get("validation_accuracy", 0.0))))

    time_reduction = None
    if baseline and optimized:
        baseline_time = float(baseline["training_time_seconds"]) if baseline.get("training_time_seconds") not in ("", None) else None
        optimized_time = float(optimized["training_time_seconds"]) if optimized.get("training_time_seconds") not in ("", None) else None
        if baseline_time is not None and optimized_time is not None and baseline_time != 0:
            time_reduction = ((baseline_time - optimized_time) / baseline_time) * 100

    gap_change = None
    if baseline and optimized:
        baseline_gap = float(baseline["train_validation_gap"]) if baseline.get("train_validation_gap") not in ("", None) else None
        optimized_gap = float(optimized["train_validation_gap"]) if optimized.get("train_validation_gap") not in ("", None) else None
        if baseline_gap is not None and optimized_gap is not None:
            gap_change = baseline_gap - optimized_gap

    lines = [
        "# CNN Controlled Experiments",
        "",
        "All experiments used the same source-image split and the same 10 discovered classes.",
        f"Split object-crop sizes: train={split_sizes['train']}, validation={split_sizes['validation']}, test={split_sizes['test']}.",
        "",
        "| Experiment | Training Time | Val Accuracy | Test Accuracy | F1 | Train-Val Gap |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in results:
        time_text = f"{float(row['training_time_seconds']):.4f}s" if row.get("training_time_seconds") not in ("", None) else ""
        val_acc = row.get("best_validation_accuracy", row.get("validation_accuracy", ""))
        val_text = f"{float(val_acc):.6f}" if val_acc not in ("", None) else ""
        test_text = f"{float(row['test_accuracy']):.6f}" if row.get("test_accuracy") not in ("", None) else ""
        f1_text = f"{float(row['f1']):.6f}" if row.get("f1") not in ("", None) else ""
        gap_text = f"{float(row['train_validation_gap']):.6f}" if row.get("train_validation_gap") not in ("", None) else ""
        lines.append(f"| {row['experiment']} | {time_text} | {val_text} | {test_text} | {f1_text} | {gap_text} |")
    best_val = float(best.get("best_validation_accuracy", best.get("validation_accuracy", 0.0)))
    lines.extend([
        "",
        f"Baseline to optimized training-time reduction: {time_reduction:.6f}%." if time_reduction is not None else "Baseline-to-optimized comparison is pending.",
        f"Baseline gap minus optimized gap: {gap_change:.6f}." if gap_change is not None else "Baseline-to-optimized gap comparison is pending.",
        f"Best validation experiment: {best['experiment']} ({best_val:.6f}).",
        "",
        "## Interpretation",
        "",
        "These are measured baseline/ablation results, not target claims. The optimized configuration was the predefined combination of extra augmentation, weight decay, dropout, scheduling, and the selected batch size; it was not chosen to match a resume number.",
        "",
        "## Configuration details",
    ])
    for row in results:
        lines.append(f"- `{row['experiment']}`: {row['configuration']}")
    (output_dir / "experiment_report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    best_model_path = output_dir / f"{best['experiment']}_best_model.pth"
    if best_model_path.exists():
        (output_dir / "best_model.pth").write_bytes(best_model_path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", default="data/raw/vehicle_images")
    parser.add_argument("--output", default="outputs/ml/experiments")
    parser.add_argument("--max-epochs", type=int, default=3)
    parser.add_argument("--experiments", default="1,2", help="Comma-separated 1-based experiment numbers, or all")
    args = parser.parse_args()
    config = Config(dataset_path=Path(args.dataset), output_path=Path(args.output), epochs=args.max_epochs)
    config.validate()
    config.output_path.mkdir(parents=True, exist_ok=True)
    set_seed(config.seed)
    samples, classes, _ = _voc_samples(Path(config.dataset_path))
    split_indices = _split_image_groups(samples, config)
    split_sizes = {"train": len(split_indices[0]), "validation": len(split_indices[1]), "test": len(split_indices[2])}
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Fixed split sizes: {split_sizes}; device: {device}; GPU: {torch.cuda.get_device_name(device) if device.type == 'cuda' else 'none'}")
    selected = EXPERIMENTS if args.experiments.strip().lower() == "all" else [EXPERIMENTS[int(value.strip()) - 1] for value in args.experiments.split(",")]
    results_path = config.output_path / "experiment_results.csv"
    results = load_results(results_path)
    completed_names = {row["experiment"] for row in results}
    for number, experiment in [(EXPERIMENTS.index(item) + 1, item) for item in selected]:
        if experiment["name"] in completed_names:
            print(f"Experiment {number}/7 already recorded; skipping: {experiment['name']}", flush=True)
            continue
        print(f"Experiment {number}/7 started: {experiment['name']}", flush=True)
        try:
            result = run_experiment(config, experiment, samples, classes, split_indices, device, config.output_path, args.max_epochs)
        except Exception as error:
            result = {field: "" for field in RESULT_FIELDS}
            result.update({"experiment": experiment["name"], "status": "failed", "error": repr(error), "configuration": json.dumps(experiment, sort_keys=True), "device": str(device)})
            print(f"Experiment {number}/7 failed: {error}", flush=True)
        else:
            print(f"Experiment {number}/7 completed: {experiment['name']}", flush=True)
        results.append(result)
        save_results(results, results_path)
        write_partial_report(results, config.output_path, split_sizes)
    successful = [row for row in results if row["status"] == "completed"]
    if successful:
        write_report(results, config.output_path, classes, split_sizes)
        best = max(successful, key=lambda row: float(row.get("best_validation_accuracy", row.get("validation_accuracy", 0.0))))
        best_model_path = config.output_path / f"{best['experiment']}_best_model.pth"
        if best_model_path.exists():
            (config.output_path / "best_model.pth").write_bytes(best_model_path.read_bytes())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
