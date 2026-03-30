import numpy as np
from utils.load_models import load_clinical_model


def run_clinical_prediction(input_df, threshold=0.5):
    bundle = load_clinical_model()
    preprocessor = bundle["preprocessor"]
    model = bundle["model"]

    X_transformed = preprocessor.transform(input_df)
    score = float(model.predict_proba(X_transformed)[:, 1][0])

    label = "PCOS" if score >= threshold else "No PCOS"
    message = (
        "Clinical pattern is more consistent with PCOS."
        if label == "PCOS"
        else "Clinical pattern is more consistent with No PCOS."
    )

    return {
        "label": label,
        "score": score,
        "threshold": threshold,
        "message": message,
    }

