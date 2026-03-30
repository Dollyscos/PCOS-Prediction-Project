from pathlib import Path
import numpy as np
import json
import joblib
import streamlit as st
from xgboost import XGBClassifier

ARTIFACT_DIR = Path(__file__).resolve().parent.parent / "artifacts"


@st.cache_resource
def load_feature_order():
    path = ARTIFACT_DIR / "clinical_feature_order.json"
    if not path.exists():
        return []
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_resource
def load_clinical_categories():
    path = ARTIFACT_DIR / "clinical_categories.json"
    if not path.exists():
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


@st.cache_resource
def load_clinical_model():
    preprocessor_path = ARTIFACT_DIR / "clinical_preprocessor.joblib"
    model_path = ARTIFACT_DIR / "clinical_xgb_model.json"

    if not preprocessor_path.exists():
        raise FileNotFoundError(f"Missing file: {preprocessor_path}")

    if not model_path.exists():
        raise FileNotFoundError(f"Missing file: {model_path}")

    preprocessor = joblib.load(preprocessor_path)

    model = XGBClassifier()
    model.load_model(str(model_path))

    return {"preprocessor": preprocessor, "model": model}


@st.cache_resource
def load_ultrasound_model():
    import tensorflow as tf  # lazy import

    model_path = ARTIFACT_DIR / "ultrasound_resnet50.keras"
    if not model_path.exists():
        raise FileNotFoundError(f"Missing file: {model_path}")

    return tf.keras.models.load_model(model_path, compile=False)


@st.cache_resource
def load_ultrasound_metadata():
    metadata_path = ARTIFACT_DIR / "ultrasound_metadata.json"
    default_metadata = {
        "img_size": [224, 224],
        "class_names": ["No PCOS", "PCOS"],
        "threshold": 0.5,
    }

    if not metadata_path.exists():
        return default_metadata

    with open(metadata_path, "r", encoding="utf-8") as f:
        return json.load(f)