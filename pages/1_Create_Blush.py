import streamlit as st
from engine.manager import create_blush

st.set_page_config(
    page_title="Create a Blush", 
    page_icon="💖"
)

st.sidebar.header("Creating a Blush!")

st.title("Create a Blush! 💖")
st.subheader("Write your feelings loud out!.")

name = st.text_input("Your Name: ", placeholder="Romeo")
password = st.text_input("Set a Secret Password: ", placeholder="Romeo")
message = st.text_area("Your Secret Message: ", placeholder="Write what you can't say out loud...", height="content")

create_code = st.button("Generate Secure Blush")

if create_code:
    if name and password and message:
        final_code = create_blush(name, message, password)
        st.success("Your Blush is ready!")
        st.code(final_code, language=None)
        st.write("Share this code with your partner. They will need the password to open it.")
    else:
        st.error("Please fill in all fields!")
    

