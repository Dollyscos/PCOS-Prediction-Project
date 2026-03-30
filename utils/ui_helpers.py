import streamlit as st


def inject_custom_css():
    st.markdown(
        """
        <style>
        .main {
            padding-top: 1rem;
        }

        .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1100px;
        }

        .hero-box {
            background: linear-gradient(135deg, #7C3AED 0%, #A855F7 100%);
            color: white;
            padding: 1.6rem 1.8rem;
            border-radius: 24px;
            margin-bottom: 1.2rem;
            box-shadow: 0 10px 30px rgba(124, 58, 237, 0.18);
        }

        .soft-card {
            background: white;
            color: black;
            border-radius: 20px;
            padding: 1.2rem 1.2rem;
            box-shadow: 0 6px 20px rgba(15, 23, 42, 0.06);
            border: 1px solid #EEE7FF;
            margin-bottom: 1rem;
        }

        .info-card {
            background: #F8F5FF;
            color: black;
            border-left: 6px solid #7C3AED;
            border-radius: 16px;
            padding: 1rem 1rem;
            margin: 0.8rem 0 1rem 0;
        }

        .success-card {
            background: #F0FDF4;
            border-left: 6px solid #16A34A;
            border-radius: 16px;
            padding: 1rem 1rem;
            margin-top: 0.8rem;
        }

        .warning-card {
            background: #FFF7ED;
            border-left: 6px solid #F97316;
            border-radius: 16px;
            padding: 1rem 1rem;
            margin-top: 0.8rem;
        }

        .section-title {
            font-size: 1.1rem;
            font-weight: 700;
            color: #4C1D95;
            margin-top: 0.5rem;
            margin-bottom: 0.7rem;
        }

        .friendly-note {
            font-size: 0.95rem;
            color: #4B5563;
            line-height: 1.6;
        }

        div.stButton > button {
            border-radius: 999px;
            padding: 0.6rem 1.2rem;
            font-weight: 600;
            border: none;
        }

        div[data-testid="stMetric"] {
            background: white;
            border: 1px solid #EEE7FF;
            padding: 0.8rem;
            border-radius: 18px;
            box-shadow: 0 6px 16px rgba(15, 23, 42, 0.05);
        }

        .small-badge {
            display: inline-block;
            background: #EDE9FE;
            color: #5B21B6;
            padding: 0.3rem 0.7rem;
            border-radius: 999px;
            font-size: 0.82rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def hero_box(title: str, subtitle: str):
    st.markdown(
        f"""
        <div class="hero-box">
            <div style="font-size: 2rem; font-weight: 800; margin-bottom: 0.35rem;">{title}</div>
            <div style="font-size: 1rem; opacity: 0.95; line-height: 1.6;">{subtitle}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def section_title(text: str):
    st.markdown(f'<div class="section-title">{text}</div>', unsafe_allow_html=True)


def info_card(title: str, body: str):
    st.markdown(
        f"""
        <div class="info-card">
            <div style="font-weight: 700; margin-bottom: 0.35rem;">{title}</div>
            <div class="friendly-note">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def success_card(body: str):
    st.markdown(f'<div class="success-card">{body}</div>', unsafe_allow_html=True)


def warning_card(body: str):
    st.markdown(f'<div class="warning-card">{body}</div>', unsafe_allow_html=True)


def soft_card(title: str, body: str):
    st.markdown(
        f"""
        <div class="soft-card">
            <div style="font-weight: 700; margin-bottom: 0.35rem;">{title}</div>
            <div class="friendly-note">{body}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def badge(text: str):
    st.markdown(f'<div class="small-badge">{text}</div>', unsafe_allow_html=True)