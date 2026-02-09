import streamlit as st
import secrets
import string
import hashlib

def code_generator():
    chars = string.ascii_uppercase + string.digits

    while True:
        code = ''.join(secrets.choice(chars) for _ in range(6))
        if code not in st.session_state.db:
            return code

def create_blush(name, message, password):
    code = code_generator()
    password_hash = hashlib.sha256(password.encode()).hexdigest()

    blush_data = {
        "sender": name,
        "message": message,
        "password": password_hash,
        "status": "unread",
        "reply": None,
        "replied_at": None
    }

    st.session_state.db[code] = blush_data

    return code



