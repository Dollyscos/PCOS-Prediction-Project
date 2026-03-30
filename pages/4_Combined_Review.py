from utils.load_models import load_clinical_categories
from utils.report_builder import build_html_report
from utils.ui_helpers import inject_custom_css, hero_box, info_card, success_card, warning_card, badge
import streamlit as st

inject_custom_css()

hero_box(
    "Final Review",
    "This page brings both prediction models together so you can compare the clinical result and the ultrasound result side by side."
)

info_card(
    "How to read this page",
    "If both predictions point in the same direction, the result appears more consistent. If they disagree, it suggests the case may need closer review."
)

clinical = st.session_state.get("clinical_result")
clinical_input = st.session_state.get("clinical_input")

ultrasound = st.session_state.get("ultrasound_result")
ultrasound_filename = st.session_state.get("ultrasound_filename")

if not clinical and not ultrasound:
    st.info(
        "No prediction results found yet. Run a clinical prediction and/or an ultrasound prediction first."
    )
    st.stop()

col1, col2 = st.columns(2)

with col1:
    st.subheader("Clinical Data Model")

    if clinical:
        st.metric("Prediction", clinical["label"])
        st.metric("Probability of PCOS", f'{clinical["score"] * 100:.2f}%')
        st.metric("Threshold", f'{clinical["threshold"] * 100:.0f}%')
        st.success(clinical["message"])

        with st.expander("Show entered clinical data"):
            if clinical_input:
                for key, value in clinical_input.items():
                    st.write(f"**{key}:** {value}")
            else:
                st.write("No saved clinical input found.")
    else:
        st.warning("No clinical result available yet.")

with col2:
    st.subheader("Ultrasound Image Model")

    if ultrasound:
        st.metric("Prediction", ultrasound["label"])
        st.metric("Probability of PCOS", f'{ultrasound["score"] * 100:.2f}%')
        st.metric("Threshold", f'{ultrasound["threshold"] * 100:.0f}%')
        st.success(ultrasound["message"])

        if ultrasound_filename:
            st.caption(f"Latest uploaded image: {ultrasound_filename}")
    else:
        st.warning("No ultrasound result available yet.")

st.divider()

st.subheader("Agreement Review")

if clinical and ultrasound:
    same_label = clinical["label"] == ultrasound["label"]

    if same_label and clinical["label"] == "PCOS":
        st.success("Agreement: both models suggest **PCOS**.")
        st.markdown(
            """
**Interpretation:**  
This case shows agreement between the two independent prediction models.

**Suggestion:**  
This shows a high case of PCOS.
"""
        )

    elif same_label and clinical["label"] == "No PCOS":
        st.success("Agreement: both models suggest **No PCOS**.")
        st.markdown(
            """
**Interpretation:**  
This case shows agreement between the two independent prediction models.

**Suggested note for demo/report:**  
This does not show any case of PCOS.
"""
        )

    else:
        st.warning("Result: the clinical and ultrasound models disagree.")
        st.markdown(
            f"""
**Clinical model:** {clinical["label"]}  
**Ultrasound model:** {ultrasound["label"]}

**Suggestion:**  
The two models do not agree on this case. This case may require closer review and more tests for confirmation.
"""
        )

else:
    st.info(
        "Only one model result is currently available. Run both prediction pages to compare them here."
    )

st.divider()
st.subheader("Download Report")

categories = load_clinical_categories()

report_html = build_html_report(
    clinical_input=st.session_state.get("clinical_input"),
    clinical_result=st.session_state.get("clinical_result"),
    clinical_shap_df=st.session_state.get("clinical_shap_df"),
    ultrasound_result=st.session_state.get("ultrasound_result"),
    ultrasound_filename=st.session_state.get("ultrasound_filename"),
    ultrasound_original_image=st.session_state.get("ultrasound_original_image"),
    ultrasound_overlay_image=st.session_state.get("ultrasound_overlay_image"),
    categories=categories,
)

st.download_button(
    label="Download Full Report",
    data=report_html,
    file_name="pcos_prediction_report.html",
    mime="text/html",
)