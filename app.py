import streamlit as st
from engine.manager import get_total_blushes, get_all_time_count, get_all_time_conf, get_total_conf
from engine.conversation import get_all_time_conversations, get_total_conversations

st.set_page_config(
    page_title="Blush | Your Secret Space",
    page_icon="💗",
    layout="wide",
    initial_sidebar_state="expanded",
)

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
    .hero {
        position: relative;
        overflow: hidden;
        border: 1px solid rgba(225, 78, 118, 0.12);
        border-radius: 28px;
        padding: 3.2rem 3rem;
        background:
            radial-gradient(circle at 88% 18%, rgba(255, 182, 193, 0.48), transparent 22rem),
            linear-gradient(135deg, #fffafa 0%, #ffecef 100%);
        margin-bottom: 1.5rem;
    }
    .hero-eyebrow {
        color: #c44569;
        font-weight: 800;
        letter-spacing: 0.16em;
        text-transform: uppercase;
        font-size: 0.76rem;
        margin-bottom: 0.7rem;
    }
    .hero h1 {
        color: #3d2a32;
        font-size: clamp(2.6rem, 6vw, 5rem);
        line-height: 0.95;
        margin: 0 0 1rem 0;
        letter-spacing: -0.055em;
    }
    .hero p {
        max-width: 650px;
        color: #745d65;
        font-size: 1.08rem;
        line-height: 1.65;
        margin-bottom: 0;
    }
    .feature-card {
        min-height: 190px;
        border: 1px solid rgba(214, 83, 120, 0.10);
        border-radius: 22px;
        background: rgba(255, 255, 255, 0.78);
        padding: 1.5rem;
        box-shadow: 0 12px 35px rgba(145, 76, 94, 0.06);
    }
    .feature-card .icon {
        display: inline-grid;
        place-items: center;
        width: 46px;
        height: 46px;
        border-radius: 14px;
        background: #ffe8ed;
        font-size: 1.35rem;
        margin-bottom: 0.85rem;
    }
    .feature-card h3 {
        color: #49353d;
        font-size: 1.05rem;
        margin: 0 0 0.45rem 0;
    }
    .feature-card p {
        color: #806a71;
        line-height: 1.55;
        margin: 0;
        font-size: 0.92rem;
    }
    [data-testid="stMetric"] {
        border: 1px solid rgba(214, 83, 120, 0.10);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.72);
        padding: 1.15rem;
        box-shadow: 0 10px 28px rgba(145, 76, 94, 0.05);
    }
    [data-testid="stMetricLabel"] {
        color: #806a71;
    }
    [data-testid="stMetricValue"] {
        color: #b83b61;
    }
    .section-title {
        color: #49353d;
        font-size: 1.45rem;
        margin: 1.8rem 0 0.85rem 0;
        letter-spacing: -0.02em;
    }
    .trust-strip {
        display: grid;
        grid-template-columns: repeat(3, 1fr);
        gap: 0.75rem;
        margin: 1.25rem 0 0.5rem 0;
    }
    .trust-item {
        border-radius: 16px;
        background: #fff8f9;
        border: 1px solid rgba(214, 83, 120, 0.08);
        padding: 1rem;
        color: #745d65;
        text-align: center;
        font-size: 0.88rem;
    }
    .footer {
        text-align: center;
        color: #9a858c;
        font-size: 0.82rem;
        margin-top: 2.5rem;
    }
    div[data-testid="stPageLink"] a {
        border-radius: 14px;
        border: 1px solid rgba(214, 83, 120, 0.11);
        background: white;
        padding: 0.75rem 0.9rem;
    }
    @media (max-width: 720px) {
        .hero { padding: 2.2rem 1.35rem; }
        .trust-strip { grid-template-columns: 1fr; }
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
<section class="hero">
    <div class="hero-eyebrow">A quieter place for honest words</div>
    <h1>Feelings, held gently. 💗</h1>
    <p>Share a secret, leave a confession, or start an anonymous conversation.
    Blush keeps the moment encrypted and ephemeral.</p>
</section>
""", unsafe_allow_html=True)

st.markdown('<h2 class="section-title">Choose what to share</h2>', unsafe_allow_html=True)

feature_col1, feature_col2, feature_col3 = st.columns(3)

with feature_col1:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">💌</div>
        <h3>Private Blush</h3>
        <p>Send a password-protected note that disappears after six hours or one read.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/1_Create_Blush.py", label="Create a private Blush", icon="🔐", use_container_width=True)

with feature_col2:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">🌸</div>
        <h3>Wall of Confessions</h3>
        <p>Post anonymously to a community wall and let the words exist for seven days.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/3_Wall_Of_Confessions.py", label="Visit the confession wall", icon="🕊️", use_container_width=True)

with feature_col3:
    st.markdown("""
    <div class="feature-card">
        <div class="icon">💬</div>
        <h3>Anonymous Conversation</h3>
        <p>Exchange messages through private Rose and Tulip identities for up to 24 hours.</p>
    </div>
    """, unsafe_allow_html=True)
    st.page_link("pages/4_Conversation.py", label="Start a conversation", icon="🌷", use_container_width=True)

st.markdown('<h2 class="section-title">Blush in numbers</h2>', unsafe_allow_html=True)

total_blushes = get_all_time_count()
db_blushes = get_total_blushes()
total_conf = get_all_time_conf()
db_conf = get_total_conf()
total_conversations = get_all_time_conversations()
db_conversations = get_total_conversations()

stat_col1, stat_col2, stat_col3 = st.columns(3)
with stat_col1:
    st.metric("Private Blushes shared", f"{total_blushes:,}", f"{db_blushes:,} waiting")
with stat_col2:
    st.metric("Public confessions", f"{total_conf:,}", f"{db_conf:,} on the wall")
with stat_col3:
    st.metric("Conversations started", f"{total_conversations:,}", f"{db_conversations:,} active")

with st.expander("How Blush protects your privacy"):
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        - **Encrypted storage:** Sensitive message content is encrypted before it reaches the database.
        - **Automatic expiry:** Content disappears after its configured lifetime.
        """)
    with col2:
        st.markdown("""
        - **Minimal collection:** No accounts or personal profiles are required.
        - **Safety checks:** Messages pass through usage safeguards before publication.
        """)

st.markdown("""
<div class="trust-strip">
    <div class="trust-item">🔒 No accounts required</div>
    <div class="trust-item">🌙 Ephemeral by design</div>
    <div class="trust-item">🌷 Anonymous by default</div>
</div>
""", unsafe_allow_html=True)

st.markdown('<div class="footer">2026 · Prashant Gupta · Developed with Blush 💗</div>', unsafe_allow_html=True)