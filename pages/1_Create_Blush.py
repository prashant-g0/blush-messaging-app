import streamlit as st

st.set_page_config(
    page_title="Create a Blush", 
    page_icon="💖"
)

st.sidebar.header("Creating a Blush!")

st.title("Create a Blush! 💖")
st.subheader("Write your feelings loud out!.")

message = st.text_area("Enter Message: ", placeholder="Write what you can't say out loud...", height="content")
create_code = st.button("Create code")

if create_code:
    if message:
        code = "x"
        st.success(f"Your code is {code}")
    else:
        st.error("Write message first.")
    

