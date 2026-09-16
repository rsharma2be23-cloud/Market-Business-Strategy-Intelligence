"""Interview-friendly convolutional classifier."""
from __future__ import annotations

import torch.nn as nn


class SimpleCNN(nn.Module):
    def __init__(self, num_classes: int, dropout: float = 0.0) -> None:
        super().__init__()
        if num_classes < 2:
            raise ValueError("At least two classes are required for classification")
        if not 0 <= dropout < 1:
            raise ValueError("dropout must be in [0, 1)")
        self.features = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(32, 64, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(64, 128, kernel_size=3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Sequential(
            nn.AdaptiveAvgPool2d((1, 1)),
            nn.Flatten(),
            nn.Dropout(dropout),
            nn.Linear(128, num_classes),
        )

    def forward(self, inputs):
        return self.classifier(self.features(inputs))
