import streamlit as st
from engine.manager import verify_and_lock, submit_reply, reject_blush, report_blush
from engine.encryption import decrypt_text
from engine.safety import is_safe, get_remote_ip

st.set_page_config(page_title="Blush | Open a Blush", page_icon="🔓")

# 1. Initialize Session State
if "auth_code" not in st.session_state:
    st.session_state.auth_code = None
    st.session_state.blush_data = None
    st.session_state.current_status = None

st.title("Unlock a Blush 🔓")

# --- PHASE 1: LOGIN (Show only if not authenticated) ---
if st.session_state.auth_code is None:
    with st.container():
        url_params = st.query_params
        default_code = url_params.get("code", "") 

        code_input = st.text_input(
            "Enter the 6-digit Secret Code:", 
            value=default_code, 
            placeholder="e.g., AB12CD"
        ).upper()

        pass_input = st.text_input("Enter the Secret Password:", type="password", placeholder="This keeps the Blush just between you two")
        st.write("Open only when you're ready!")
        if st.button("Open Gently 🌸"):
            if code_input and pass_input:
                success, data, status = verify_and_lock(code_input, pass_input)
                
                if success:
                    # Bypassing the loop: Save to session state and rerun
                    st.session_state.auth_code = code_input
                    st.session_state.temp_pass = pass_input
                    st.session_state.blush_data = data
                    st.session_state.current_status = status
                    st.rerun()
                else:
                    # Access Denial Messages
                    if status == "reading":
                        st.error("🔒 Access Denied: Someone else is reading this Blush right now.")
                    elif status == "rejected":
                        st.error("🚫 This Blush was left unanswered.")
                    elif status == "opened":
                        st.info("💗 This Blush held a beautiful exchange, but its moment has now passed.")
                    elif status == "reported":
                        st.error("This message is been reported and under observation.")
                    else:
                        st.error(data) # "Incorrect password" or "Code not found"
            else:
                st.warning("Both keys are needed to unlock this Blush.")

# --- PHASE 2: INTERACTION (Show after successful Unlock) ---
else:
    code = st.session_state.auth_code
    pass_input = st.session_state.temp_pass
    data = st.session_state.blush_data
    status = st.session_state.current_status

    # UI for UNREAD messages (Now in 'reading' state in DB)
    if status == "reading":
        st.snow()
        st.success(f"A Blush from {data['sender_name']} is waiting for you!")
        st.write("---")
        decrypted_message = decrypt_text(data['message'], pass_input)
        st.text_area(label="The Blush, Just for you:",value=decrypted_message, height="content")
        
        st.write("### Your Response")
        reply_text = st.text_area("Write a reply...", placeholder="What's on your mind...", max_chars=500)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            if st.button("Send Reply 💗"):
                if not is_safe(reply_text): st.error("⚠️ This reply contains flagged language. Please keep it respectful.")
                elif reply_text:
                    if submit_reply(code, reply_text, pass_input):
                        st.success("The Blush continues 🌷")
                        # Clear session so they can't see it again
                        del st.session_state.temp_pass
                        st.session_state.auth_code = None 
                        st.rerun()
                else:
                    st.warning("Say at least one honest line.")
        
        with col2:
            if st.button("Let It Stay Unanswered"):
                if reject_blush(code):
                    st.warning("Message rejected.")
                    del st.session_state.temp_pass
                    st.session_state.auth_code = None
                    st.rerun()
        
        with col3:
            if st.button("⚠️ Report"):
                current_ip = get_remote_ip()
                if report_blush(code, current_ip):
                    st.warning("Thank you. We'll review usage patterns to keep Blush safe.")
                    st.session_state.clear()
                    st.rerun()

    # UI for REPLIED messages (Now transitioning to 'opened')
    elif status == "replied":
        st.write("### The Final Exchange")
        st.subheader(f"From {data['sender_name']}:")
        original_msg = decrypt_text(data['message'], pass_input)
        st.text_area("Your Message:", value=original_msg, height="content",  disabled=True)

        decrypted_reply = decrypt_text(data['reply'], pass_input)
        st.text_area("Their Reply:", value=decrypted_reply, height="content", disabled=True)
        
        
        st.toast("This Blush will fade away soon.")
        
        if st.button("Close the Blush 💗"):
            st.session_state.auth_code = None
            st.rerun()

st.markdown("<p style='text-align: center; color:#888;'>2026 | Prashant Gupta | Developed with Blush 💗</p>", unsafe_allow_html=True)