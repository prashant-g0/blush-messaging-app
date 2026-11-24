import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from engine.manager import create_blush
from engine.safety import is_safe, get_remote_ip, creation_clearance
from engine.theme import inject_theme, page_header, page_footer

st.set_page_config(
    page_title="Blush | Create a Blush", 
    page_icon="💖",
    layout="wide",
)

inject_theme()
page_header(
    "Private Blush",
    "Write a Blush! 💖",
    "Write what your heart has been holding back. The note is encrypted and designed to disappear.",
)

with st.container():
    with st.container(border=True):
        name = st.text_input(
            "Sender name",
            placeholder="e.g. Romeo",
            max_chars=20
        )

        password = st.text_input(
            "Secret password",
            type="password",
            placeholder="Choose something only they would know",
            max_chars=10
        )

        message = st.text_area(
            "Your Blush",
            placeholder="Take a breath before you write...",
            height=180,
            max_chars=500
        )

        agree = st.checkbox(
            "I agree to use Blush responsibly."
        )

        create_clicked = st.button(
            "Lock this feeling 🔐",
            type="primary",
            use_container_width=True
        )
        
if create_clicked:
    user_ip = get_remote_ip()
    allow, error = creation_clearance(user_ip)
    if name and password and message:
        if not agree:
            st.error("Please confirm responsible use to continue.")
        elif not allow:
            st.warning(error)
        elif not is_safe(message):
            st.error("This message might cross our usage boundaries.")
        else:
            with st.spinner("Wrapping your feelings in a little privacy..."):
                final_code = create_blush(name, message, password, user_ip)

            if final_code:
                st.balloons()
                shareable_link = f"https://blushnow.streamlit.app/Open_Blush?code={final_code}"
                invite_text = f"Hey! I left a secret message for you on Blush. 🌸\n\nLink: {shareable_link}\nPassword: {password}\n\n(This will vanish in 6 hours!)"
                st.success("Your Blush is ready.")
                st.code(shareable_link)
                st_copy_to_clipboard(invite_text, before_copy_label="Copy invitation", after_copy_label="Copied")
            else:
                st.error("The Blush slipped for a moment. Please try again.")
    else:
        st.warning("Every Blush needs all its petals.")

page_footer()
