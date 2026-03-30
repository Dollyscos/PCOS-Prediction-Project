import numpy as np
from tensorflow.keras.applications.resnet50 import preprocess_input


def predict_ultrasound(model, pil_image, metadata):
    img_size = tuple(metadata.get("img_size", [224, 224]))
    class_names = metadata.get("class_names", ["No PCOS", "PCOS"])
    threshold = float(metadata.get("threshold", 0.5))

    image = pil_image.resize(img_size).convert("RGB")
    arr = np.array(image).astype("float32")
    arr = np.expand_dims(arr, axis=0)
    

    pred = model.predict(arr, verbose=0)
    score = float(np.array(pred).ravel()[0])

    positive_label = class_names[1] if len(class_names) > 1 else "PCOS"
    negative_label = class_names[0] if len(class_names) > 0 else "No PCOS"
    label = positive_label if score >= threshold else negative_label

    message = (
        "Ultrasound pattern is more consistent with PCOS."
        if label == positive_label
        else "Ultrasound pattern is more consistent with No PCOS."
    )

    return {
        "label": label,
        "score": score,
        "threshold": threshold,
        "message": message,
    }

