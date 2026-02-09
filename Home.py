import streamlit as st

if "db" not in st.session_state:
    st.session_state.db = {}

st.set_page_config(
    page_title="Blush",
    page_icon="💗"
)

st.title("Blush 💗")
st.subheader("Some words are meant to be read only once.")

st.write("""
         Welcome to Blush. Create a secret message for your loved ones that
         disappears forever once it's been read.

         **Use the sidebar on the left to get started!**
""")

st.info("👈 Select 'Create Blush' to write a message.")
