import numpy as np
import pandas as pd
import shap
import streamlit as st
import matplotlib.pyplot as plt

from utils.load_models import load_clinical_model
from utils.clinical_form_config import get_display_label


def _resolve_column_list(cols, input_columns):
    if isinstance(cols, slice):
        return list(input_columns[cols])

    if isinstance(cols, (list, tuple, pd.Index, np.ndarray)):
        resolved = []
        for c in cols:
            if isinstance(c, (int, np.integer)):
                resolved.append(str(input_columns[c]))
            else:
                resolved.append(str(c))
        return resolved

    if isinstance(cols, str):
        return [cols]

    return [str(c) for c in cols]


def _extract_names_from_transformer(transformer, cols):
    if transformer == "drop":
        return []

    if transformer == "passthrough":
        return list(cols)

    try:
        names = transformer.get_feature_names_out(cols)
        return [str(x) for x in names]
    except Exception:
        pass

    if hasattr(transformer, "named_steps"):
        try:
            names = transformer.get_feature_names_out(cols)
            return [str(x) for x in names]
        except Exception:
            pass

        for _, step in reversed(list(transformer.named_steps.items())):
            try:
                names = step.get_feature_names_out(cols)
                return [str(x) for x in names]
            except Exception:
                continue

    return list(cols)


def _get_transformed_feature_names(preprocessor, input_columns, n_features):
    names = []

    try:
        names = list(preprocessor.get_feature_names_out(input_columns))
    except Exception:
        try:
            names = list(preprocessor.get_feature_names_out())
        except Exception:
            names = []

    if not names and hasattr(preprocessor, "transformers_"):
        for _, transformer, cols in preprocessor.transformers_:
            if transformer == "drop":
                continue

            resolved_cols = _resolve_column_list(cols, input_columns)
            names.extend(_extract_names_from_transformer(transformer, resolved_cols))

    names = [str(x) for x in names]

    if len(names) > n_features:
        names = names[:n_features]
    elif len(names) < n_features:
        names.extend([f"feature_{i+1}" for i in range(len(names), n_features)])

    return names


def _extract_shap_row(shap_values, n_features):
    arr = np.asarray(shap_values)

    if arr.ndim == 3:
        if arr.shape[1] == n_features:
            row = arr[0, :, -1]
        elif arr.shape[2] == n_features:
            row = arr[0, -1, :]
        else:
            row = arr.reshape(-1)

    elif arr.ndim == 2:
        row = arr[0]

    elif arr.ndim == 1:
        row = arr

    else:
        row = arr.reshape(-1)

    row = np.asarray(row).reshape(-1)

    if len(row) > n_features:
        row = row[:n_features]
    elif len(row) < n_features:
        row = np.pad(row, (0, n_features - len(row)), constant_values=0.0)

    return row


def _normalize_text(text):
    return "".join(ch.lower() for ch in str(text) if ch.isalnum())


def _map_transformed_to_original(transformed_name, raw_columns):
    name = str(transformed_name)

    if "__" in name:
        name = name.split("__", 1)[1]

    raw_columns_sorted = sorted(raw_columns, key=len, reverse=True)
    norm_name = _normalize_text(name)

    for col in raw_columns_sorted:
        norm_col = _normalize_text(col)

        if norm_name == norm_col:
            return col

        if norm_name.startswith(norm_col):
            return col

    return name


@st.cache_resource
def get_shap_explainer():
    bundle = load_clinical_model()
    model = bundle["model"]

    if hasattr(model, "get_booster"):
        return shap.TreeExplainer(model.get_booster())

    return shap.TreeExplainer(model)


def explain_clinical_prediction(input_df: pd.DataFrame, top_n: int = 8) -> pd.DataFrame:
    bundle = load_clinical_model()
    preprocessor = bundle["preprocessor"]

    X_transformed = preprocessor.transform(input_df)
    if hasattr(X_transformed, "toarray"):
        X_dense = X_transformed.toarray()
    else:
        X_dense = np.asarray(X_transformed)

    n_features = X_dense.shape[1]
    transformed_names = _get_transformed_feature_names(
        preprocessor=preprocessor,
        input_columns=list(input_df.columns),
        n_features=n_features,
    )

    explainer = get_shap_explainer()
    shap_values = explainer.shap_values(X_dense)
    shap_row = _extract_shap_row(shap_values, n_features=n_features)

    transformed_df = pd.DataFrame({
        "Transformed feature": transformed_names,
        "SHAP value": shap_row,
    })

    transformed_df["Original feature"] = transformed_df["Transformed feature"].apply(
        lambda x: _map_transformed_to_original(x, list(input_df.columns))
    )

    grouped_df = (
        transformed_df.groupby("Original feature", as_index=False)["SHAP value"]
        .sum()
        .copy()
    )

    grouped_df["Feature"] = grouped_df["Original feature"].apply(get_display_label)
    grouped_df["Absolute impact"] = grouped_df["SHAP value"].abs()
    grouped_df["Direction"] = np.where(
        grouped_df["SHAP value"] >= 0,
        "Pushes toward PCOS",
        "Pushes toward No PCOS",
    )

    grouped_df = (
        grouped_df.sort_values("Absolute impact", ascending=False)
        .head(top_n)
        .reset_index(drop=True)
    )

    return grouped_df[["Feature", "Direction", "SHAP value", "Absolute impact"]]


def plot_shap_bar(shap_df: pd.DataFrame):
    plot_df = shap_df.sort_values("SHAP value", ascending=True)

    fig, ax = plt.subplots(figsize=(8, max(4, 0.55 * len(plot_df))))
    ax.barh(plot_df["Feature"], plot_df["SHAP value"])
    ax.axvline(0, linewidth=1)
    ax.set_xlabel("SHAP value")
    ax.set_ylabel("")
    ax.set_title("Top input contributions (importance)")
    fig.tight_layout()
    return fig