import streamlit as st
from engine.manager import get_total_blushes, get_all_time_count

st.set_page_config(
    page_title="Blush",
    page_icon="💗",
    layout="centered"
)

st.markdown("<h1 style='text-align: center;'>Blush 💗</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color:#888;'>Encrypted. Ephemeral. one-time</p>", unsafe_allow_html=True)

st.divider()
st.subheader("The one-time, encrypted secret messenger for your feelings.")

total_count = get_all_time_count()
db_count = get_total_blushes()

col1, col2 = st.columns(2)
with col1:
    st.metric(label="Total Blushes Shared All-Time", value=f"{total_count} 💖")

with col2:
    st.metric(label="Stored Blushes", value=f"{db_count} 😍")

st.divider()

st.write("""
         Blush allows you to send a message that burns after it's been read.
         No accounts, no tracking, just pure expressions.

         **Use the sidebar on the left to get started!**
""")

st.info("👈 Select 'Create Blush' to write a message.")

with st.expander("How it works & Privacy"):
    st.write("""
            - **Encryption:** Your message is encrypted with your password *before* it reaches our database (AES-256).
            - **Auto-Purge:** Every message is automatically deleted from our servers 6 hours after creation.
            - **One-Shot:** Once a conversation cycle (open -> reply) is complete, the access code expires.
""")
