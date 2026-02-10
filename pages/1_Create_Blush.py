import streamlit as st
from engine.manager import create_blush

st.set_page_config(
    page_title="Create a Blush", 
    page_icon="💖"
)

st.sidebar.header("Creating a Blush!")

st.title("Create a Blush! 💖")
st.subheader("Write your feelings loud out!.")

name = st.text_input("Your Name: ", placeholder="e.g., Romeo")
password = st.text_input("Set a Secret Password: ", type="password", placeholder="Keep it secret!")
message = st.text_area("Your Secret Message: ", placeholder="Write what you can't say out loud...", height="content")

if st.button("Generate Secure Blush"):
    if name and password and message:
        with st.spinner("Locking your secret in the valut..."):
            final_code = create_blush(name, message, password)
        
        if final_code:
            st.success("Your Blush is ready!")
            st.balloons()

        st.write("Share this code:")
        st.code(final_code, language=None)

        st.info("💡Your partner needs this code AND the password to unlock the message.")
    else:
        st.error("Something went wrong with the database. Please try again!")
else:
    st.warning("Please fill in all fields to create your Blush.")
    

