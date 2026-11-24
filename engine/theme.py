import streamlit as st


def inject_theme():
    st.markdown("""
    <style>
        .block-container {
            max-width: 1180px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #fff4f6 0%, #fffafa 100%);
        }
        .page-hero {
            border: 1px solid rgba(225, 78, 118, 0.12);
            border-radius: 28px;
            padding: 2.25rem 2.4rem;
            background:
                radial-gradient(circle at 88% 18%, rgba(255, 182, 193, 0.42), transparent 22rem),
                linear-gradient(135deg, #fffafa 0%, #ffecef 100%);
            margin-bottom: 1.35rem;
        }
        .page-hero .eyebrow {
            color: #c44569;
            font-weight: 800;
            letter-spacing: 0.14em;
            text-transform: uppercase;
            font-size: 0.72rem;
            margin-bottom: 0.55rem;
        }
        .page-hero h1 {
            color: #3d2a32;
            font-size: clamp(2.2rem, 5vw, 3.8rem);
            line-height: 1;
            letter-spacing: -0.045em;
            margin: 0 0 0.65rem 0;
        }
        .page-hero p {
            color: #745d65;
            max-width: 700px;
            margin: 0;
            line-height: 1.55;
        }
        .blush-panel {
            border: 1px solid rgba(214, 83, 120, 0.10);
            border-radius: 22px;
            background: rgba(255, 255, 255, 0.82);
            padding: 1.45rem;
            box-shadow: 0 12px 35px rgba(145, 76, 94, 0.06);
        }
        [data-testid="stTextInput"] input,
        [data-testid="stTextArea"] textarea {
            border-radius: 14px !important;
            border-color: rgba(214, 83, 120, 0.16) !important;
        }
        .stButton > button {
            border-radius: 14px;
            border: 1px solid rgba(214, 83, 120, 0.14);
            min-height: 46px;
            font-weight: 700;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(135deg, #d95d7d, #b83b61);
            border: none;
        }
        [data-testid="stChatMessage"] {
            border: 1px solid rgba(214, 83, 120, 0.08);
            border-radius: 18px;
            background: rgba(255, 248, 249, 0.82);
            padding: 0.8rem 1rem;
        }
        [data-testid="stChatInput"] textarea {
            border-radius: 18px !important;
        }
        [data-testid="stMetric"] {
            border: 1px solid rgba(214, 83, 120, 0.10);
            border-radius: 18px;
            background: rgba(255, 255, 255, 0.72);
            padding: 1.15rem;
            box-shadow: 0 10px 28px rgba(145, 76, 94, 0.05);
        }
        [data-testid="stMetricValue"] { color: #b83b61; }
        [data-testid="stMetricLabel"] { color: #806a71; }
        .blush-footer {
            text-align: center;
            color: #9a858c;
            font-size: 0.82rem;
            margin-top: 2.5rem;
        }
        @media (max-width: 720px) {
            .page-hero { padding: 1.7rem 1.25rem; }
        }
    </style>
    """, unsafe_allow_html=True)


def page_header(eyebrow, title, description):
    st.markdown(
        f"""
        <section class="page-hero">
            <div class="eyebrow">{eyebrow}</div>
            <h1>{title}</h1>
            <p>{description}</p>
        </section>
        """,
        unsafe_allow_html=True,
    )


def page_footer():
    st.markdown(
        '<div class="blush-footer">2026 · Prashant Gupta · Developed with Blush 💗</div>',
        unsafe_allow_html=True,
    )
