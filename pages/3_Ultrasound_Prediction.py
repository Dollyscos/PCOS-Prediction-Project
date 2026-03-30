import streamlit as st
from PIL import Image

from utils.load_models import load_ultrasound_model, load_ultrasound_metadata
from utils.ultrasound_prediction import predict_ultrasound
from utils.gradcam_utils import (
    make_gradcam_heatmap_resnet_manual,
    overlay_gradcam_on_pil,
)
from utils.ui_helpers import inject_custom_css, hero_box, info_card, success_card


inject_custom_css()

hero_box(
    "Ultrasound Prediction",
    "Upload an ultrasound image to receive a prediction and a visual explanation showing where the model focused most."
)



def get_gradcam_explanation(pred_label: str, score: float) -> str:
    pct = score * 100

    if pred_label == "PCOS":
        return f"""
### What the highlighted area means

The coloured heatmap shows the parts of the ultrasound image that had the **strongest influence** on the model's decision.

- **Red and yellow areas** = the model paid the most attention to these parts
- **Green areas** = these parts had a moderate influence on the prediction
- **Blue and darker areas** = the model relied on these parts less

In this case, the model predicted **PCOS** with a probability of **{pct:.2f}%**, with the highlighted region appearing to correspond to areas that may reflect follicle patterns, which were commonly emphasised in other PCOS predictions during testing.

### Simple explanation
You can think of Grad-CAM as showing **where the model looked most carefully before making its decision.**

### Important note
The highlighted region does **not automatically mean abnormality by itself**. It only shows which area influenced the AI model most during prediction.
"""
    return f"""
### What the highlighted area means

The coloured heatmap shows the parts of the ultrasound image that had the **strongest influence** on the model's decision.

- **Red and yellow areas** = the model paid the most attention to these parts
- **Green areas** = these parts had a moderate influence on the prediction
- **Blue and darker areas** = the model relied on these parts less

In this case, the model predicted **No PCOS** with a probability of **{pct:.2f}%**.

### Simple explanation
Grad-CAM helps show **which part of the image mattered most to the model**, not just the final answer.

### Important note
The heatmap is an **explanation of model attention**, not a medical diagnosis on its own.
"""


model = load_ultrasound_model()
metadata = load_ultrasound_metadata()

uploaded_file = st.file_uploader(
    "Upload an ultrasound image",
    type=["png", "jpg", "jpeg"]
)

if uploaded_file is not None:
    image = Image.open(uploaded_file).convert("RGB")
    st.image(image, caption="Uploaded ultrasound image", use_container_width=True)

    if st.button("Predict from Ultrasound"):
        result = predict_ultrasound(model, image, metadata)

        st.session_state["ultrasound_result"] = result
        st.session_state["ultrasound_filename"] = uploaded_file.name
        st.session_state["ultrasound_original_image"] = image.copy()

        c1, c2, c3 = st.columns(3)
        c1.metric("Prediction", result["label"])
        c2.metric("Probability", f'{result["score"] * 100:.2f}%')
        c3.metric("Threshold", f'{result["threshold"] * 100:.0f}%')

        success_card(f"<b>Result summary:</b> {result['message']}")

        try:
            class_index = 1 if result["label"] == "PCOS" else 0

            heatmap, _ = make_gradcam_heatmap_resnet_manual(
                pil_image=image,
                model=model,
                class_index=class_index,
                img_size=tuple(metadata.get("img_size", [224, 224]))
            )

            overlay = overlay_gradcam_on_pil(image, heatmap, alpha=0.35)
            st.session_state["ultrasound_overlay_image"] = overlay.copy()

            col1, col2 = st.columns(2)
            with col1:
                st.image(image, caption="Original image", use_container_width=True)
            with col2:
                st.image(overlay, caption="Grad-CAM overlay", use_container_width=True)

            st.markdown(get_gradcam_explanation(result["label"], result["score"]))

        except Exception as e:
            st.warning(f"Grad-CAM preview unavailable: {e}")