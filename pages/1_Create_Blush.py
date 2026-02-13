import streamlit as st
from engine.manager import create_blush
from engine.safety import is_safe, get_remote_ip, creation_clearance

st.set_page_config(
    page_title="Create a Blush", 
    page_icon="💖"
)


st.title("Write a Blush! 💖")
st.subheader("Write what your heart has been holding back!")

name = st.text_input("This is how they'll know it's from you: ", placeholder="e.g., Romeo", max_chars=20)
password = st.text_input("Set a Secret Password: ", type="password", placeholder="Something only they would guess...", max_chars=10)
message = st.text_area("Your Blush: ", placeholder="Take a breath before you write....", height="content", max_chars=500)
st.write("This message can be read only once.")

user_ip = get_remote_ip()
allow, error = creation_clearance(user_ip)

agree = st.checkbox("I agree to use Blush responsibly.")
if st.button("🔐Lock this Feeling"):
    if name and password and message:
        if not agree: st.error("Please confirm responsible use to continue.")
        elif not allow: st.warning(f"{error}")
        elif not is_safe(message): st.error("⚠️ This message might cross our usage boundaries. Please rephrase it.")
        else:
            with st.spinner("Wrapping your feelings in a little privacy...💗"):
                final_code = create_blush(name, message, password, user_ip)

                if final_code:
                    st.balloons()

                    base_url = "http://localhost:8501/Open_Blush" 
                    shareable_link = f"{base_url}?code={final_code}"
                    invite_text = f"Hey! You've received a Blush from {name} 🌸\nIt's meant to be opened just once.\n\nLink: {shareable_link}\nPassword: {password}"
                    
                    
                    st.write("### Share them carefully:")
                    st.code(invite_text, language=None)
                    st.caption("Click the copy icon in the top right of thr box above.")
                    
                else:
                    st.error("The Blush slipped for a moment. Please try again!")
    else:
        st.warning("Every Blush needs all its petals.")
