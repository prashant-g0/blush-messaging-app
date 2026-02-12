import streamlit as st
from engine.manager import verify_and_lock, submit_reply, reject_blush

st.set_page_config(page_title="Open a Blush", page_icon="🔓")

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
                    else:
                        st.error(data) # "Incorrect password" or "Code not found"
            else:
                st.warning("Both keys are needed to unlock this Blush.")

# --- PHASE 2: INTERACTION (Show after successful Unlock) ---
else:
    code = st.session_state.auth_code
    data = st.session_state.blush_data
    status = st.session_state.current_status

    # UI for UNREAD messages (Now in 'reading' state in DB)
    if status == "reading":
        st.snow()
        st.success(f"A Blush from {data['sender_name']} is waiting for you!")
        st.write("---")
        st.write("The Blush, Just for you:")
        st.text_area(data['message'], height="content")
        
        st.write("### Your Response")
        reply_text = st.text_area("Write a reply...", placeholder="What's on your mind...", max_chars=500)
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send Reply 💗"):
                if reply_text:
                    if submit_reply(code, reply_text):
                        st.success("The Blush continues 🌷")
                        # Clear session so they can't see it again
                        st.session_state.auth_code = None 
                        st.rerun()
                else:
                    st.warning("Say at least one honest line.")
        
        with col2:
            if st.button("Let It Stay Unanswered"):
                if reject_blush(code):
                    st.warning("Message rejected.")
                    st.session_state.auth_code = None
                    st.rerun()

    # UI for REPLIED messages (Now transitioning to 'opened')
    elif status == "replied":
        st.write("### The Final Exchange")
        st.subheader(f"From {data['sender_name']}:")
        st.info(data['message'])
        
        st.subheader("Their Reply:")
        st.success(data['reply'])
        
        st.toast("This Blush will fade away soon.")
        
        if st.button("Close the Blush 💗"):
            st.session_state.auth_code = None
            st.rerun()

st.markdown("<p style='text-align: center; color:#888;'>2026 | Prashant Gupta | Developed with Blush 💗</p>", unsafe_allow_html=True)