"""Torch-free metric helpers for classification outputs."""
from __future__ import annotations

import json
from pathlib import Path

from PIL import Image, ImageDraw

def confusion_matrix(labels: list[int], predictions: list[int], num_classes: int) -> list[list[int]]:
    matrix = [[0 for _ in range(num_classes)] for _ in range(num_classes)]
    for label, prediction in zip(labels, predictions):
        matrix[label][prediction] += 1
    return matrix


def classification_metrics(labels: list[int], predictions: list[int], num_classes: int) -> dict:
    matrix = confusion_matrix(labels, predictions, num_classes)
    true_positive = [matrix[index][index] for index in range(num_classes)]
    precisions, recalls, f1_scores = [], [], []
    for index in range(num_classes):
        predicted_positive = sum(row[index] for row in matrix)
        actual_positive = sum(matrix[index])
        precision = true_positive[index] / predicted_positive if predicted_positive else 0.0
        recall = true_positive[index] / actual_positive if actual_positive else 0.0
        f1 = 2 * precision * recall / (precision + recall) if precision + recall else 0.0
        precisions.append(precision)
        recalls.append(recall)
        f1_scores.append(f1)
    total = len(labels)
    accuracy = sum(label == prediction for label, prediction in zip(labels, predictions)) / total if total else 0.0
    per_class = {
        str(index): {"precision": precisions[index], "recall": recalls[index], "f1": f1_scores[index]}
        for index in range(num_classes)
    }
    return {
        "accuracy": accuracy,
        "macro_precision": sum(precisions) / num_classes,
        "macro_recall": sum(recalls) / num_classes,
        "macro_f1": sum(f1_scores) / num_classes,
        "confusion_matrix": matrix,
        "per_class": per_class,
        "classification_report": per_class,
    }


def save_metrics(metrics: dict, path: Path) -> None:
    path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")


def save_classification_report(metrics: dict, classes: list[str], path: Path) -> None:
    lines = ["class precision recall f1-score"]
    for index, name in enumerate(classes):
        values = metrics["per_class"][str(index)]
        lines.append(f"{name} {values['precision']:.6f} {values['recall']:.6f} {values['f1']:.6f}")
    lines.extend([
        "",
        f"accuracy {metrics['accuracy']:.6f}",
        f"macro_precision {metrics['macro_precision']:.6f}",
        f"macro_recall {metrics['macro_recall']:.6f}",
        f"macro_f1 {metrics['macro_f1']:.6f}",
    ])
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def save_confusion_matrix_png(metrics: dict, classes: list[str], path: Path) -> None:
    matrix = metrics["confusion_matrix"]
    cell_size, margin = 42, 180
    image = Image.new("RGB", (margin + cell_size * len(classes), margin + cell_size * len(classes)), "white")
    draw = ImageDraw.Draw(image)
    for row, values in enumerate(matrix):
        for column, value in enumerate(values):
            x, y = margin + column * cell_size, margin + row * cell_size
            draw.rectangle((x, y, x + cell_size, y + cell_size), outline="black")
            draw.text((x + 15, y + 13), str(value), fill="black")
    for index, name in enumerate(classes):
        draw.text((margin + index * cell_size + 3, margin - 18), str(index), fill="black")
        draw.text((5, margin + index * cell_size + 13), str(index), fill="black")
    image.save(path)
