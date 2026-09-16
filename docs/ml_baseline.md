# CNN Baseline

## Status

The baseline was run on 2026-09-16 using the real KaggleHub download in the workspace-selected `.venv`.

## Dataset

The input is the public sample of DataCluster Labs' Indian Vehicle Dataset. Acquisition details and provenance are in [ml_dataset_setup.md](ml_dataset_setup.md). KaggleHub downloaded version 5 to its local cache; the original 100 JPEGs and 100 Pascal VOC XML files were copied unchanged into `data/raw/vehicle_images/`.

The archive is annotation-oriented rather than class-folder-oriented. It contains 100 images with 100 Pascal VOC files and 331 labeled object instances across 10 classes. The loader uses each annotated bounding box as one classification crop and splits by source image, so crops from one image cannot cross train, validation, and test partitions.

Observed class counts: `auto` 59, `bicycle` 14, `bus` 32, `car` 52, `concrete_mixer` 11, `tempo` 13, `tractor` 22, `truck_tanker` 11, `two_wheelers` 82, `vehicle_truck` 35. All 100 JPEGs were readable; no corrupted images were found.

## Preprocessing

- Pascal VOC XML annotations are parsed from the raw directory.
- Classes are discovered from `<object><name>` labels.
- A deterministic source-image split uses 70% train, 15% validation, and 15% test object crops.
- The split is created before transforms and has disjoint indices, preventing image leakage between partitions.
- Training: resize to 128 x 128, random horizontal flip, small random rotation, tensor conversion, ImageNet mean/std normalization.
- Validation/test: resize to 128 x 128, tensor conversion, ImageNet mean/std normalization.
- Batch size, workers, seed, and paths are configurable in `src/ml/config.py` or by CLI arguments.

## CNN architecture

`SimpleCNN` contains three convolution/ReLU/max-pooling blocks, adaptive average pooling, and a fully connected classifier. The final linear layer is created with the discovered number of classes.

## Training

- Loss: cross-entropy
- Optimizer: Adam
- Default learning rate: `0.001`
- Default epochs: `20`
- Default early-stopping patience: `5`
- Best checkpoint criterion: lowest validation loss
- Reproducibility: seed `42`, seeded Python/NumPy/PyTorch RNGs, deterministic cuDNN settings

## Device reporting

The run selects CUDA only when `torch.cuda.is_available()` returns true. Otherwise it uses CPU. The run prints the device and GPU name when CUDA is actually detected. No GPU usage is inferred from configuration alone.

## Exact command

From the repository root, after installing dependencies and placing the dataset:

```text
python -m pip install -r requirements.txt
python -m src.ml.train --dataset data/raw/vehicle_images --output outputs/ml/baseline
```

To override baseline hyperparameters:

```text
python -m src.ml.train --epochs 20 --batch-size 32 --learning-rate 0.001
```

## Outputs

A completed run writes:

- `outputs/ml/baseline/best_model.pth`
- `outputs/ml/baseline/training_history.csv`
- `outputs/ml/baseline/metrics.json`
- `outputs/ml/baseline/test_metrics.json`
- `outputs/ml/baseline/classification_report.txt`
- `outputs/ml/baseline/confusion_matrix.png`
- `outputs/ml/baseline/run_metadata.json`

The metrics JSON contains accuracy, macro precision, macro recall, macro F1, per-class classification-report values, and the confusion matrix. These are calculated from the test predictions and are never hard-coded.

## Actual results

- Device: `cpu`
- GPU: none detected (`torch 2.14.0+cpu`, `torchvision 0.29.0+cpu`)
- Dataset object crops: 331
- Train/validation/test: 236 / 57 / 38 object crops
- Classes: 10
- Batch size: 32
- Epochs completed: 20
- Learning rate: 0.001
- Training time: 465.7503 seconds
- Best epoch: 20
- Validation accuracy at best epoch: 0.4210526 (42.1053%)
- Test accuracy: 0.2631579 (26.3158%)
- Test macro precision: 0.0344828 (3.4483%)
- Test macro recall: 0.0909091 (9.0909%)
- Test macro F1: 0.0500000 (5.0000%)

The results are baseline measurements only. This small, imbalanced object-crop sample is not evidence of a 90%+ validation-accuracy claim. No optimization, GPU acceleration, or comparative experiment was performed.
