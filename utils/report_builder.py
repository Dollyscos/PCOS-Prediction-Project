from datetime import datetime
import io
import base64
import pandas as pd

from utils.clinical_form_config import (
    get_display_label,
    format_category_value,
    is_binary_feature,
    is_cycle_feature,
)
from utils.shap_explainability import plot_shap_bar


def _fig_to_base64(fig) -> str:
    buf = io.BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight", dpi=150)
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return encoded


def _pil_to_base64(img) -> str:
    if img is None:
        return ""
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    buf.seek(0)
    encoded = base64.b64encode(buf.read()).decode("utf-8")
    buf.close()
    return encoded


def _format_clinical_inputs(clinical_input: dict, categories: dict) -> pd.DataFrame:
    rows = []

    for feature, value in clinical_input.items():
        display_value = (
            format_category_value(feature, value)
            if (feature in categories or is_binary_feature(feature) or is_cycle_feature(feature))
            else value
        )

        rows.append({
            "Field": get_display_label(feature),
            "Value": display_value
        })

    return pd.DataFrame(rows)


def _format_shap_rows(shap_df: pd.DataFrame) -> str:
    if shap_df is None or shap_df.empty:
        return "<p>No explanation available.</p>"

    rows_html = ""
    for _, row in shap_df.iterrows():
        rows_html += f"""
        <tr>
            <td>{row['Feature']}</td>
            <td>{row['Direction']}</td>
            <td>{float(row['SHAP value']):.4f}</td>
        </tr>
        """

    return f"""
    <table style="width:100%; border-collapse: collapse;" border="1" cellpadding="8">
        <thead style="background:#f3f0ff;">
            <tr>
                <th>Input</th>
                <th>Direction</th>
                <th>SHAP Value</th>
            </tr>
        </thead>
        <tbody>
            {rows_html}
        </tbody>
    </table>
    """


def build_html_report(
    clinical_input=None,
    clinical_result=None,
    clinical_shap_df=None,
    ultrasound_result=None,
    ultrasound_filename=None,
    ultrasound_original_image=None,
    ultrasound_overlay_image=None,
    categories=None,
):
    categories = categories or {}
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    clinical_input_html = "<p>No clinical input available.</p>"
    if clinical_input:
        df = _format_clinical_inputs(clinical_input, categories)
        clinical_input_html = df.to_html(index=False, escape=False)

    clinical_summary_html = "<p>No clinical prediction available.</p>"
    if clinical_result:
        clinical_summary_html = f"""
        <ul>
            <li><strong>Prediction:</strong> {clinical_result['label']}</li>
            <li><strong>Probability of PCOS:</strong> {clinical_result['score'] * 100:.2f}%</li>
            <li><strong>Interpretation:</strong> {clinical_result['message']}</li>
        </ul>
        """

    shap_html = "<p>No explanation available.</p>"
    shap_plot_html = ""
    if clinical_shap_df is not None and not clinical_shap_df.empty:
        shap_html = _format_shap_rows(clinical_shap_df)
        fig = plot_shap_bar(clinical_shap_df)
        shap_plot_b64 = _fig_to_base64(fig)
        shap_plot_html = f"""
        <div style="margin: 12px 0;">
            <img src="data:image/png;base64,{shap_plot_b64}" style="max-width:100%; border-radius:12px; border:1px solid #ddd;" />
        </div>
        """

    ultrasound_summary_html = "<p>No ultrasound prediction available.</p>"
    if ultrasound_result:
        ultrasound_summary_html = f"""
        <ul>
            <li><strong>Prediction:</strong> {ultrasound_result['label']}</li>
            <li><strong>Probability of PCOS:</strong> {ultrasound_result['score'] * 100:.2f}%</li>
            <li><strong>Interpretation:</strong> {ultrasound_result['message']}</li>
            <li><strong>Uploaded image:</strong> {ultrasound_filename or 'Not available'}</li>
        </ul>
        """

    original_img_html = "<p>No original ultrasound image available.</p>"
    if ultrasound_original_image is not None:
        original_b64 = _pil_to_base64(ultrasound_original_image)
        original_img_html = f"""
        <img src="data:image/png;base64,{original_b64}" style="max-width:100%; border-radius:12px; border:1px solid #ddd;" />
        """

    overlay_img_html = "<p>No color-coded overlay available.</p>"
    if ultrasound_overlay_image is not None:
        overlay_b64 = _pil_to_base64(ultrasound_overlay_image)
        overlay_img_html = f"""
        <img src="data:image/png;base64,{overlay_b64}" style="max-width:100%; border-radius:12px; border:1px solid #ddd;" />
        """

    if clinical_result and ultrasound_result:
        if clinical_result["label"] == ultrasound_result["label"]:
            agreement_html = f"""
            <p><strong>Agreement:</strong> Yes</p>
            <p>Both models point toward <strong>{clinical_result["label"]}</strong>.</p>
            <p>This shows a high case of PCOS.</p>
            """
        else:
            agreement_html = f"""
            <p><strong>Agreement:</strong> No</p>
            <p>The clinical data model predicted <strong>{clinical_result["label"]}</strong>, while the ultrasound image model predicted <strong>{ultrasound_result["label"]}</strong>.</p>
            <p>This means the two models do not match and the case may need closer review and more tests for confirmation.</p>
            """
    else:
        agreement_html = "<p>Only one model result is currently available.</p>"

    gradcam_explanation = """
    <p>The colour-coded heatmap highlights the regions of the ultrasound image that had the strongest influence on the model's prediction. In the case of PCOS, the highlighted region appears to correspond to areas that may reflect follicle patterns, which were commonly emphasised in other PCOS predictions during testing.</p>
    <ul>
        <li><strong>Red / yellow</strong>: strongest influence</li>
        <li><strong>Green</strong>: moderate influence</li>
        <li><strong>Blue / dark areas</strong>: lower influence</li>
    </ul>
    <p>This does not diagnose PCOS by itself. It only shows where the model focused most.</p>
    """

    suggestions_html = """
    <ul>
        <li>The predictions should be interpreted together with symptoms, history, and professional clinical assessment.</li>
        <li>Discordant results may require closer review rather than a single conclusion.</li>
    </ul>
    """

    html = f"""
    <html>
    <head>
        <meta charset="utf-8">
        <title>PCOS Prediction Report</title>
    </head>
    <body style="font-family: Arial, sans-serif; padding: 24px; color: #1f2937; line-height: 1.6;">
        <h1 style="color:#6d28d9;">PCOS Prediction Report</h1>
        <p><strong>Generated on:</strong> {timestamp}</p>

        <hr>


        <h2 style="color:#7c3aed;">Clinical Prediction</h2>
        {clinical_summary_html}

        <h2 style="color:#7c3aed;">Explanation of Clinical Data Prediction</h2>
        <p>The plot below shows which clinical inputs most influenced the clinical data prediction.</p>
        {shap_plot_html}
        {shap_html}

        <h2 style="color:#7c3aed;">Ultrasound Prediction Summary</h2>
        {ultrasound_summary_html}

        <h2 style="color:#7c3aed;">Ultrasound Images</h2>
        <table style="width:100%; border-collapse: collapse;">
            <tr>
                <td style="width:50%; padding-right:12px; vertical-align:top;">
                    <h3>Original image</h3>
                    {original_img_html}
                </td>
                <td style="width:50%; padding-left:12px; vertical-align:top;">
                    <h3>Colour-coded overlay</h3>
                    {overlay_img_html}
                </td>
            </tr>
        </table>

        <h2 style="color:#7c3aed;">Explanation of Ultrasound Image Prediction</h2>
        {gradcam_explanation}

        <h2 style="color:#7c3aed;">Combined Review</h2>
        {agreement_html}

        <h2 style="color:#7c3aed;">Interpretation and Suggestions</h2>
        {suggestions_html}

        <h2 style="color:#7c3aed;">Clinical Input Details</h2>
        {clinical_input_html}

        <hr>
        <p style="font-size: 0.9rem; color:#6b7280;">
            This report was generated by the PCOS prediction system for educational and decision-support purposes.
        </p>
    </body>
    </html>
    """

    return html