import streamlit as st
from engine.manager import get_total_blushes

st.set_page_config(
    page_title="Blush",
    page_icon="💗"
)

st.title("Welcome to Blush 💗")
st.subheader("### The one-time, encrypted secret messenger for your feelings.")

total_count = get_total_blushes()
st.metric(label="Total Blushes Created", value=f"{total_count} 💖")

st.divider()

st.write("""
         Blush allows you to send a message that burns after it's been read.
         No accounts, no tracking, just pure expressions.

         **Use the sidebar on the left to get started!**
""")

st.info("👈 Select 'Create Blush' to write a message.")
