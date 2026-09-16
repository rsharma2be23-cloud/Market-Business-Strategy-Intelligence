# CNN Controlled Experiments

This document is generated and updated after the sequential experiment runner completes. It compares the existing baseline behavior with one controlled change at a time, followed by a predefined combined configuration.

## Experimental control

- Dataset: DataCluster Labs Indian Vehicle Dataset, using the downloaded Pascal VOC annotations.
- Classes: discovered from the 10 observed XML object labels.
- Split: one source-image split generated once with seed 42 and reused by every experiment.
- Object crops from one source image remain in the same partition.
- Baseline behavior preserves the existing baseline transform: resize, horizontal flip, and small rotation.
- The augmentation experiment adds random resized crop to that baseline.
- No experiment is selected to match a desired resume metric.

## Experiments

1. Baseline: existing batch size, transforms, optimizer, and no weight decay, dropout, or scheduler.
2. Batch: batch size 16 instead of 32.
3. Augmentation: adds random resized crop while retaining the existing baseline augmentation.
4. Regularization: adds Adam weight decay of `1e-4`.
5. Dropout: adds classifier dropout of `0.30`.
6. Learning-rate scheduling: adds `ReduceLROnPlateau` with factor `0.5` and patience `2`.
7. Optimized: combines extra augmentation, weight decay, dropout, scheduler, and the selected batch size.

## Reproduction

From the repository root, using the project environment:

```text
python -m src.ml.experiments --dataset data/raw/vehicle_images --output outputs/ml/experiments --epochs 20
```

CUDA is selected only when `torch.cuda.is_available()` is true. Otherwise all experiments run on CPU. Each run resets the random seeds and uses the fixed split.

## Results

The runner writes measured values to `outputs/ml/experiments/experiment_results.csv` and the comparison table to `outputs/ml/experiments/experiment_report.md`. Per-experiment histories are stored in subdirectories. This section is updated with actual results after execution; no values are prefilled.

## Limitations

The source sample contains 100 images and 331 labeled object instances spread across 10 classes, with strong class imbalance. Results are baseline/ablation evidence for this small sample, not a production benchmark or a general claim about Indian vehicle recognition. Training-time comparisons are specific to the observed hardware and runtime and do not establish GPU acceleration unless CUDA is actually detected.
