import streamlit as st
from engine.manager import create_blush

st.set_page_config(
    page_title="Create a Blush", 
    page_icon="💖"
)

st.sidebar.header("Creating a Blush!")

st.title("Create a Blush! 💖")
st.subheader("Write your feelings loud out!.")

name = st.text_input("Your Name: ", placeholder="e.g., Romeo", max_chars=20)
password = st.text_input("Set a Secret Password: ", type="password", placeholder="Keep it secret!", max_chars=10)
message = st.text_area("Your Secret Message: ", placeholder="Write what you can't say out loud...", height="content", max_chars=500)

if st.button("Generate Secure Blush"):
    if name and password and message:
        with st.spinner("Locking your secret in the valut..."):
            final_code = create_blush(name, message, password)

            if final_code:
                st.balloons()
    
                base_url = "http://localhost:8501/Open_Blush" 
                shareable_link = f"{base_url}?code={final_code}"
                invite_text = f"Hey! You have a Blush message from {name} 💖\n\nLink: {shareable_link}\nPassword: {password}"
                
                
                st.write("### Share this with them:")
                st.code(invite_text, language=None)
                st.caption("Click the copy icon in the top right of thr box above.")
                
                st.info("💡 Share either the code or the link. Your partner will still need the password!")
            else:
                st.error("Something went wrong with the database. Please try again!")
    else:
        st.warning("Please fill in all fields to create your Blush.")
