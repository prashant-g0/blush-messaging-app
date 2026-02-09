import streamlit as st

st.set_page_config(
    page_title="Open a Blush", 
    page_icon="💝"
)

st.sidebar.header("Opening a Blush!")

st.title("Decoding you message 💝")
st.subheader("Take a breath before you open this.")

code = st.text_input("Enter your code here: ", placeholder="XLC4c3")
decode = st.button("Open Blush")

if decode:
    if code and len(code)==6:
        message = "hi"
        st.text_area("Your message:", value=f"{message}", height="content")
    else:
        st.error("Enter correct code first")



