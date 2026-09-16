"""Configuration for the reproducible baseline CNN."""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Config:
    seed: int = 42
    image_size: int = 128
    batch_size: int = 32
    learning_rate: float = 1e-3
    epochs: int = 20
    num_workers: int = 0
    patience: int = 5
    train_fraction: float = 0.70
    validation_fraction: float = 0.15
    dataset_path: Path = field(default_factory=lambda: Path("data/raw/vehicle_images"))
    output_path: Path = field(default_factory=lambda: Path("outputs/ml/baseline"))

    @property
    def test_fraction(self) -> float:
        return 1.0 - self.train_fraction - self.validation_fraction

    def validate(self) -> None:
        if self.image_size <= 0 or self.batch_size <= 0 or self.epochs <= 0:
            raise ValueError("image_size, batch_size, and epochs must be positive")
        if self.learning_rate <= 0 or self.patience < 0:
            raise ValueError("learning_rate must be positive and patience cannot be negative")
        if self.train_fraction <= 0 or self.validation_fraction <= 0 or self.test_fraction <= 0:
            raise ValueError("train, validation, and test fractions must all be positive")

    def as_dict(self) -> dict:
        values = self.__dict__.copy()
        values["dataset_path"] = str(values["dataset_path"])
        values["output_path"] = str(values["output_path"])
        values["test_fraction"] = self.test_fraction
        return values
