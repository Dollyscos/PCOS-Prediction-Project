from utils.ui_helpers import inject_custom_css, hero_box, section_title
import streamlit as st
import pandas as pd

from utils.load_models import load_feature_order, load_clinical_categories
from utils.clinical_form_config import (
    SECTION_ORDER,
    get_section,
    get_display_label,
    format_category_value,
    get_numeric_step,
    is_binary_feature,
    get_binary_options,
    is_cycle_feature,
)

inject_custom_css()

hero_box(
    "Clinical Prediction",
    "Make sure to enter the available values as accurately as possible."
)

feature_order = load_feature_order()
categories = load_clinical_categories()

if not feature_order:
    st.error("clinical_feature_order.json was not found or is empty.")
    st.stop()

grouped_features = {section: [] for section in SECTION_ORDER}
for feature in feature_order:
    section = get_section(feature)
    if section not in grouped_features:
        grouped_features[section] = []
    grouped_features[section].append(feature)

inputs = {}

with st.form("clinical_form"):
    for section in SECTION_ORDER:
        features = grouped_features.get(section, [])
        if not features:
            continue

        section_title(section)
        cols = st.columns(2)

        for i, feature in enumerate(features):
            label = get_display_label(feature)

            with cols[i % 2]:
                if is_binary_feature(feature):
                    options = get_binary_options()
                    inputs[feature] = st.selectbox(
                        label,
                        options,
                        format_func=lambda x, f=feature: format_category_value(f, x),
                        key=f"clinical_{feature}",
                    )

                elif is_cycle_feature(feature):
                    options = categories.get(feature, [0, 1])
                    inputs[feature] = st.selectbox(
                        label,
                        options,
                        format_func=lambda x, f=feature: format_category_value(f, x),
                        key=f"clinical_{feature}",
                    )

                elif feature in categories and len(categories[feature]) > 0:
                    options = categories[feature]
                    inputs[feature] = st.selectbox(
                        label,
                        options,
                        format_func=lambda x, f=feature: format_category_value(f, x),
                        key=f"clinical_{feature}",
                    )

                else:
                    inputs[feature] = st.number_input(
                        label,
                        value=0.0,
                        step=get_numeric_step(feature),
                        key=f"clinical_{feature}",
                    )

        st.markdown("---")

    submitted = st.form_submit_button("Predict from Clinical Data")

if submitted:
    from utils.clinical_prediction import run_clinical_prediction
    from utils.shap_explainability import explain_clinical_prediction

    input_df = pd.DataFrame([inputs])
    result = run_clinical_prediction(input_df)
    shap_df = explain_clinical_prediction(input_df, top_n=8)

    st.session_state["clinical_input"] = inputs
    st.session_state["clinical_result"] = result
    st.session_state["clinical_shap_df"] = shap_df

if "clinical_result" in st.session_state:
    result = st.session_state["clinical_result"]

    c1, c2, c3 = st.columns(3)
    c1.metric("Prediction", result["label"])
    c2.metric("Probability of PCOS", f'{result["score"] * 100:.2f}%')
    c3.metric("Threshold", f'{result["threshold"] * 100:.0f}%')

    st.success(result["message"])

    with st.expander("Show entered clinical data"):
        pretty_rows = []
        current_inputs = st.session_state.get("clinical_input", {})
        for feature, value in current_inputs.items():
            pretty_rows.append(
                {
                    "Field": get_display_label(feature),
                    "Value": format_category_value(feature, value)
                    if (feature in categories or is_binary_feature(feature) or is_cycle_feature(feature))
                    else value,
                }
            )
        st.dataframe(pd.DataFrame(pretty_rows), use_container_width=True, hide_index=True)

    if "clinical_shap_df" in st.session_state:
        from utils.shap_explainability import plot_shap_bar

        shap_df = st.session_state["clinical_shap_df"]

        st.subheader("Why the model made this prediction")
        st.caption("Positive values push the prediction toward PCOS. Negative values push it toward No PCOS.")

        fig = plot_shap_bar(shap_df)
        st.pyplot(fig, use_container_width=True)

        display_df = shap_df.copy()
        display_df["SHAP value"] = display_df["SHAP value"].round(4)
        display_df["Absolute impact"] = display_df["Absolute impact"].round(4)

        st.dataframe(
            display_df[["Feature", "Direction", "SHAP value", "Absolute impact"]],
            use_container_width=True,
            hide_index=True,
        )