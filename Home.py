import streamlit as st
from engine.manager import get_total_blushes, get_all_time_count, get_all_time_conf, get_total_conf

st.set_page_config(
    page_title="Blush | Your Secret Vault ",
    page_icon="💗",
    layout="centered"
)

with st.container(border=True):
    st.markdown("<h1 style='text-align: center;'>Blush 💗</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#888;'>Encrypted. Ephemeral. Just once</p>", unsafe_allow_html=True)

    st.divider()
    st.subheader("""
                A one-time, encrypted note for the words you can't say twice.
                Whether it's a private secret meant for one, or a public confession meant for the world. 
    """)

total_blushes = get_all_time_count()
db_blushes = get_total_blushes()

total_conf = get_all_time_conf()
db_conf = get_total_conf()

col1, col2 = st.columns(2)
with col1:
    with st.container(border=True):
        st.markdown("### Private Blushes")
        st.metric(label="**All Time Shared!**", value=f"{total_blushes} 💖")
        st.metric(label="**Waiting to be Read**", value=f"{db_blushes} 😍")

with col2:
    with st.container(border=True):
        st.markdown("### 🕊️ Public Confessions")
        st.metric(label="**Total Confessions**", value=f"{total_conf} 💌")
        st.metric(label="**Currently on the Wall**", value=f"{db_conf} 📨")

st.divider()

st.info("👈 Use the sidebar to **Create a Blush** or visit the **Wall of Confessions**.")

st.write("""
        Blush is where you leave a note that doesn't stay.
        It's a quiet place for honest feelings - shared once, then gone.
         
        Choose your path:
        1. **Private Blush:** An encrypted, one-time message for a specific person.
        2. **Wall of Confessions:** A public, anonymous post on our community board.
        """)


with st.container():
    with st.expander("How it works & Privacy"):
        st.write("""
                - **Private Encryption:** Private messages use AES-256 encryption. We cannot read them.
                - **Auto-Purge:** Private messages vanish after 6 hours. Public confessions vanish after 7 days.
                - **Zero Tracking:** No accounts, no history, and no personal logs.
    """)
        
    with st.expander("Usage & Safety Policy"):
        st.write("""
                - **Safety Engine:** All messages (public & private) pass through a safety filter to prevent abuse.
                - **Anonymity:** We don't store your identity, but we apply minimal safeguards to discourage misuse.
                - **No Storage:** We are a transit point, not an archive. Once it's gone, it's gone forever.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("We don't store identities.")
    with col2:
        st.write("We don't track views.")
    with col3:
        st.write("We don't keep copies.")

st.subheader("Blush 💗, Where feelings find a safe place to go.")
st.markdown("<p style='text-align: center; color:#888;'>2026 | Prashant Gupta | Developed with Blush 💗</p>", unsafe_allow_html=True)