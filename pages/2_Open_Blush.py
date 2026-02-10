import streamlit as st
from engine.manager import verify_and_lock, submit_reply, reject_blush

st.set_page_config(page_title="Open a Blush", page_icon="🔓")

st.title("Unlock a Blush 🔓")

# 1. Entry Phase
with st.container():
    code = st.text_input("Enter the 6-digit Secret Code:", placeholder="e.g., AB12CD").upper()
    password = st.text_input("Enter the Secret Password:", type="password")
    unlock_btn = st.button("Unlock Secret")

if unlock_btn:
    if code and password:
        # Call the manager to check credentials and handle state transitions
        success, data, status = verify_and_lock(code, password)

        if success:
            # CASE: UNREAD -> Now transitioning to READING
            if status == "reading":
                st.balloons()
                st.success(f"A message from {data['sender_name']} has been unlocked!")
                st.write("---")
                st.subheader("The Secret Message:")
                st.info(data['message'])
                
                # Option to Reply or Reject
                st.write("### Your Response")
                reply_text = st.text_area("Write a reply...", placeholder="What's on your mind?")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("Send Reply"):
                        if reply_text:
                            if submit_reply(code, reply_text):
                                st.success("Reply sent! The love cycle continues.")
                                st.rerun()
                        else:
                            st.warning("Please write something before replying.")
                
                with col2:
                    if st.button("Don't Reply (Reject)"):
                        if reject_blush(code):
                            st.warning("Message rejected. Redirecting...")
                            st.rerun()

            # CASE: REPLIED -> Now transitioning to OPENED
            elif status == "replied":
                st.write("### The Final Conversation")
                st.text_area("Original Message:", value=data['message'], disabled=True)
                st.text_area("The Reply:", value=data['reply'], disabled=True)
                st.toast("This message is now archived and will expire soon.")

        else:
            # ACCESS DENIAL PHASE (Mocking the blocks)
            if status == "reading":
                st.error("🔒 Access Denied: This message is currently being read or the session was interrupted.")
            elif status == "rejected":
                st.error("🚫 This message was rejected by your partner.")
            elif status == "opened":
                st.info("⌛ This code had a good covo, but the love cycle of this message has ended.")
            else:
                st.error(data) # Shows "Incorrect password" or "Code not found"
    else:
        st.warning("Please enter both the code and the password.")