import streamlit as st
from utils.ui_helpers import inject_custom_css, hero_box, info_card

st.set_page_config(
    page_title="PCOS Decision Support Dashboard",
    page_icon="🩺",
    layout="wide",
)

inject_custom_css()

hero_box(
    "PCOS PREDICTION SYSTEM",
    "A simple space to explore PCOS prediction from clinical tests and symptom details, ultrasound images, or both together."
)

info_card(
    "Important note",
    "This platform is designed for educational and decision-support use. It does not replace a doctor’s diagnosis."
)

st.markdown("## To start your prediction")
st.write(
    "Use the sidebar to move between the Home page, Clinical Prediction, Ultrasound Prediction, Final Review, and About page."
)