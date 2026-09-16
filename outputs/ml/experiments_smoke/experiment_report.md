# CNN Controlled Experiments

All experiments used the same source-image split and the same 10 discovered classes.
Split object-crop sizes: train=236, validation=57, test=38.

| Experiment | Training Time | Val Accuracy | Test Accuracy | F1 | Train-Val Gap |
|---|---:|---:|---:|---:|---:|
| baseline | 91.2904s | 0.210526 | 0.315789 | 0.080876 | 0.108460 |
| batch | 90.8951s | 0.210526 | 0.421053 | 0.133333 | 0.052186 |

Baseline-to-optimized comparison is pending.
Baseline-to-optimized gap comparison is pending.
Best validation experiment: baseline (0.210526).

## Interpretation

These are measured baseline/ablation results, not target claims. The optimized configuration was the predefined combination of extra augmentation, weight decay, dropout, scheduling, and the selected batch size; it was not chosen to match a resume number.

## Configuration details
- `baseline`: {"batch_size": 32, "dropout": 0.0, "extra_augmentation": false, "name": "baseline", "scheduler": false, "weight_decay": 0.0}
- `batch`: {"batch_size": 16, "dropout": 0.0, "extra_augmentation": false, "name": "batch", "scheduler": false, "weight_decay": 0.0}
