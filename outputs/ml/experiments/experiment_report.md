# CNN Controlled Experiments

All experiments used the same source-image split and the same 10 discovered classes.
Split object-crop sizes: train=236, validation=57, test=38.

| Experiment | Training Time | Val Accuracy | Test Accuracy | F1 | Train-Val Gap |
|---|---:|---:|---:|---:|---:|
| baseline | 91.2904s | 0.210526 | 0.315789 | 0.080876 | 0.108460 |
| batch | 90.8951s | 0.210526 | 0.421053 | 0.133333 | 0.052186 |
| augmentation | 79.9516s | 0.192982 | 0.315789 | 0.116190 | 0.125409 |
| regularization | 72.1672s | 0.210526 | 0.315789 | 0.080876 | 0.090916 |
| dropout | 71.1248s | 0.210526 | 0.368421 | 0.092941 | 0.066087 |
| lr_schedule | 69.1127s | 0.210526 | 0.315789 | 0.080876 | 0.108460 |
| optimized | 70.7210s | 0.192982 | 0.263158 | 0.067972 | 0.053375 |

Baseline to optimized training-time reduction: 22.531789%.
Baseline gap minus optimized gap: 0.055085.
Best validation experiment: baseline (0.210526).

## Interpretation

These are measured baseline/ablation results, not target claims. The optimized configuration was the predefined combination of extra augmentation, weight decay, dropout, scheduling, and the selected batch size; it was not chosen to match a resume number.

## Configuration details
- `baseline`: {"batch_size": 32, "dropout": 0.0, "extra_augmentation": false, "name": "baseline", "scheduler": false, "weight_decay": 0.0}
- `batch`: {"batch_size": 16, "dropout": 0.0, "extra_augmentation": false, "name": "batch", "scheduler": false, "weight_decay": 0.0}
- `augmentation`: {"batch_size": 32, "dropout": 0.0, "extra_augmentation": true, "name": "augmentation", "scheduler": false, "weight_decay": 0.0}
- `regularization`: {"batch_size": 32, "dropout": 0.0, "extra_augmentation": false, "name": "regularization", "scheduler": false, "weight_decay": 0.0001}
- `dropout`: {"batch_size": 32, "dropout": 0.3, "extra_augmentation": false, "name": "dropout", "scheduler": false, "weight_decay": 0.0}
- `lr_schedule`: {"batch_size": 32, "dropout": 0.0, "extra_augmentation": false, "name": "lr_schedule", "scheduler": true, "weight_decay": 0.0}
- `optimized`: {"batch_size": 32, "dropout": 0.3, "extra_augmentation": true, "name": "optimized", "scheduler": true, "weight_decay": 0.0001}
