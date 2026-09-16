# Vehicle Image Dataset Input

The downloaded sample is stored here unchanged. Do not commit synthetic images or relabeled files.

Actual downloaded layout:

```text
data/raw/vehicle_images/
    *.jpg
    *.xml
```

The archive uses Pascal VOC XML annotations rather than class folders. The training code discovers class names from XML `<object><name>` labels, crops each annotated bounding box, and splits by source image. The exact classes present in the acquired sample are authoritative; do not create empty or invented classes.
