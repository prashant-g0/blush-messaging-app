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
        code_input = st.text_input("Enter the 6-digit Secret Code:").upper()
        pass_input = st.text_input("Enter the Secret Password:", type="password")
        
        if st.button("Unlock Secret"):
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
                        st.error("🔒 Access Denied: Someone is currently reading this.")
                    elif status == "rejected":
                        st.error("🚫 This message was rejected by your partner.")
                    elif status == "opened":
                        st.info("⌛ This code had a good covo, but the love cycle of this message has ended.")
                    else:
                        st.error(data) # "Incorrect password" or "Code not found"
            else:
                st.warning("Please enter both credentials.")

# --- PHASE 2: INTERACTION (Show after successful Unlock) ---
else:
    code = st.session_state.auth_code
    data = st.session_state.blush_data
    status = st.session_state.current_status

    # UI for UNREAD messages (Now in 'reading' state in DB)
    if status == "reading":
        st.balloons()
        st.success(f"A message from {data['sender_name']} has been unlocked!")
        st.write("---")
        st.subheader("The Secret Message:")
        st.info(data['message'])
        
        st.write("### Your Response")
        reply_text = st.text_area("Write a reply...", placeholder="What's on your mind?")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("Send Reply"):
                if reply_text:
                    if submit_reply(code, reply_text):
                        st.success("Reply sent! The cycle continues.")
                        # Clear session so they can't see it again
                        st.session_state.auth_code = None 
                        st.rerun()
                else:
                    st.warning("Please write something first.")
        
        with col2:
            if st.button("Don't Reply (Reject)"):
                if reject_blush(code):
                    st.warning("Message rejected.")
                    st.session_state.auth_code = None
                    st.rerun()

    # UI for REPLIED messages (Now transitioning to 'opened')
    elif status == "replied":
        st.write("### The Final Conversation")
        st.subheader(f"From {data['sender_name']}:")
        st.info(data['message'])
        
        st.subheader("Your Partner's Reply:")
        st.success(data['reply'])
        
        st.toast("This message is now archived and will expire soon.")
        
        if st.button("Finish & Exit"):
            st.session_state.auth_code = None
            st.rerun()