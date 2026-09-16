# CNN Dataset Setup

## Selected dataset

**Indian Vehicle Dataset** by DataCluster Labs.

- Dataset page: https://github.com/datacluster-labs/Indian-Vehicle-Dataset
- Public sample link: https://www.kaggle.com/datasets/dataclusterlabs/indian-vehicle-dataset
- Original dataset description: more than 50,000 Indian vehicle images captured/crowdsourced from more than 1,000 Indian urban and rural areas, manually reviewed by DataCluster Labs
- Image capture period stated by the publisher: 2020-2022
- Publisher-stated classes: Indian Auto, Indian Truck, Bus, Truck, Tempo Traveller, Tractor, Car, Two Wheelers
- Publisher: DataCluster Labs
- License: no license was identified in the repository README; verify the current Kaggle/DataCluster Labs terms before redistribution or commercial use

This is a real public sample link, not a generated project dataset. The full dataset is described by the publisher as available by request; the Kaggle sample is the practical baseline input.

## Download

1. Open the public Kaggle page in a browser: https://www.kaggle.com/datasets/dataclusterlabs/indian-vehicle-dataset
2. Use Kaggle's Download button and complete any normal Kaggle account or access prompts. Do not bypass access controls.
3. Extract the downloaded archive.
4. Copy the image class directories into `data/raw/vehicle_images/` without renaming labels or changing image contents.
5. Keep any dataset README/license file beside the images for provenance.

The publisher's README also provides a contact route for the full collection: `sales@datacluster.ai`. The automated Kaggle API download was not completed in this environment, so no image archive or metrics are claimed here.

## Actual directory structure

```text
data/raw/vehicle_images/
    image_001.jpg
    image_001.xml
    image_002.jpg
    image_002.xml
```

The downloaded sample uses Pascal VOC XML object annotations. The pipeline discovers the observed object classes from the XML files, crops the annotated boxes, and keeps all crops from a source image in the same split. It does not create images, labels, or classes.

## Run after setup

Install the project dependencies, then run from the repository root:

```text
python -m src.ml.train --dataset data/raw/vehicle_images --output outputs/ml/baseline
```

The training code creates deterministic train/validation/test splits by class, applies augmentation only to training images, and writes measured artifacts under `outputs/ml/baseline/`.
