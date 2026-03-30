import streamlit as st
from utils.ui_helpers import inject_custom_css, hero_box, soft_card, info_card, badge

inject_custom_css()

hero_box(
    "PCOS PREDICTION SYSTEM",
    "This platform lets you explore PCOS prediction in two ways: from clinical tests and symptom details, and from ultrasound images."
)

st.markdown("### What is Polycystic Ovary Syndrome (PCOS)?")
st.write("Polycystic Ovary Syndrome (PCOS) is a hormonal condition that affects some women in their reproductive age. The condition is characterised by hormonal imbalances, irregular menstruation, hyperandrogenism, and even excessive hair growth.")

col1, col2 = st.columns(2)

with col1:
    badge("Clinical Data Prediction")
    soft_card(
        "Predict from clinical details",
        "Enter information like cycle pattern, symptoms, hormone values, and scan-related findings as accurately as possible to get a prediction from the AI model."
    )

with col2:
    badge("Ultrasound Image Prediction")
    soft_card(
        "Predict from an ultrasound image",
        "Upload an ultrasound image to get a prediction from the AI model."
    )

st.markdown("### What you can do here")
c1, c2, c3 = st.columns(3)

with c1:
    soft_card("Clinical prediction", "Get a prediction from the AI model and understand which factors influenced it most.")

with c2:
    soft_card("Ultrasound prediction", "Get a prediction from the AI model and a simple visual explanation showing which area influenced it most.")

with c3:
    soft_card("Final review", "Compare both results side by side and see whether they agree or disagree.")

info_card(
    "Simple explanation",
    "Think of this platform as a friendly guide. It is meant to support understanding, not to replace medical judgment."
)