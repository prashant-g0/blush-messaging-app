import streamlit as st
from engine.manager import get_total_blushes, get_all_time_count

st.set_page_config(
    page_title="Blush",
    page_icon="💗",
    layout="centered"
)

with st.container(border=True):
    st.markdown("<h1 style='text-align: center;'>Blush 💗</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color:#888;'>Encrypted. Ephemeral. Just once</p>", unsafe_allow_html=True)

    st.divider()
    st.subheader("""
                A one-time, encrypted note for the words you can't say twice.
                A Private space to share what your heart won't repeat.
                For feelings meant to be read once, and felt forever.  
    """)

    total_count = get_all_time_count()
    db_count = get_total_blushes()

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label="**Blushes Shared, All Time!**", value=f"{total_count} 💖")

    with col2:
        st.metric(label="**Blushes Still Waiting to be Read.**", value=f"{db_count} 😍")

st.divider()

st.write("""
         Blush lets you send a message that disappears the moment it's read.\n
         **No account. No tracking. No history**.\n
         Just a quiet place for honest feelings - Shared once, then gone.\n
         **Lucky if they reply,  because then it becomes a complete conversation.**
         \n\n
         Blush is where you leave a note that doesn't stay.\n
         It's read once, felt deeply, and then it fades - **just like some moments should**.
""")

st.info("👈 Select 'Create Blush' from the sidebar.")
with st.container():
    with st.expander("How it works & Privacy"):
        st.write("""
                - **Encryption:** Your message is encrypted with your password *before* it reaches our database (AES-256).
                - **Auto-Purge:** Every message is automatically deleted from our servers 6 hours after creation.
                - **One-Shot:** Once a conversation cycle (open -> reply) is complete, the access code expires.
    """)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("We don't store identities.")
    with col2:
        st.write("We don't track views.")
    with col3:
        st.write("We don't keep copies.")

st.subheader("Blush it! because some words are better when they don't linger.")
st.markdown("<p style='text-align: center; color:#888;'>2026 | Prashant Gupta | Developed with Blush 💗</p>", unsafe_allow_html=True)