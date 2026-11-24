import streamlit as st
from st_copy_to_clipboard import st_copy_to_clipboard
from streamlit_autorefresh import st_autorefresh
from datetime import datetime, timezone

from engine.conversation import (
    create_conversation,
    get_by_creator_token,
    get_by_public_token,
    authenticate_recipient,
    authenticate_creator,
    get_conversation_messages,
    get_message_count,
    send_conversation_reply,
)
from engine.safety import is_safe
from engine.theme import inject_theme, page_header, page_footer

st.set_page_config(
    page_title="Blush | Conversation", 
    page_icon="💬",
    layout="wide")

inject_theme()
page_header(
    "Anonymous conversation",
    "Private words, flower identities 💬",
    "A password-protected conversation that expires after 24 hours or 10 messages.",
)

params = st.query_params


def get_authenticated_conversations():
    if "authenticated_conversations" not in st.session_state:
        st.session_state.authenticated_conversations = {}
    return st.session_state.authenticated_conversations


def start_chat_autorefresh():
    st_autorefresh(interval=10000, key="chat_refresh")


def conversation_status(conversation):
    if conversation["status"] == "expired":
        st.error("🪴 Conversation Expired\n\nThis conversation has expired.")
        return
    if conversation["status"] == "closed":
        st.error("🌸 Conversation Ended\n\nMaximum messages reached.")
    elif conversation["status"] == "active":
        st.success("💗 Conversation Active")


def get_base_url():
    try:
        return str(st.context.url).rstrip("/")
    except Exception:
        return "https://blushnow.streamlit.app/Conversation"


def show_home():
    form_col, info_col = st.columns([1.7, 0.8], gap="large")
    with form_col:
        with st.container(border=True):
            initial_message = st.text_area(
                "Initial message",
                placeholder="Write the first message...",
                height=150,
                max_chars=500,
            )
            password = st.text_input(
                "Conversation password",
                type="password",
                max_chars=100,
            )
            agree = st.checkbox("I agree to use this conversation responsibly.")
            create_clicked = st.button("Create conversation 🌸", type="primary", use_container_width=True)

    with info_col:
        st.markdown("""
        <div class="blush-panel">
            <h3>Anonymous identities</h3>
            <p>🌹 Creator — Rose<br>
            🌷 Recipient — Tulip<br><br>
            ⏳ 24-hour lifetime<br>
            💬 Maximum 10 messages</p>
        </div>
        """, unsafe_allow_html=True)

    if create_clicked:
        if not initial_message or not password:
            st.warning("Add both an initial message and a password.")
        elif not agree:
            st.warning("Please confirm responsible use.")
        elif not is_safe(initial_message):
            st.error("This message might cross our usage boundaries.")
        else:
            try:
                created = create_conversation(initial_message, password)
                base_url = get_base_url()
                recipient_link = f"{base_url}?chat={created['public_token']}"
                creator_link = f"{base_url}?manage={created['creator_token']}"

                st.success("Conversation created.")
                st.markdown("### Recipient Link")
                st.code(recipient_link)
                st_copy_to_clipboard(
                    recipient_link,
                    before_copy_label="Copy recipient link",
                    after_copy_label="Recipient link copied",
                )

                st.markdown("### 🔐 Private Creator Management Link")
                st.warning(
                    "Save this private link now. It is shown only once and cannot be recovered."
                )
                st.code(creator_link)
                st_copy_to_clipboard(
                    creator_link,
                    before_copy_label="Copy creator link",
                    after_copy_label="Creator link copied",
                )
            except Exception as exc:
                st.error("The conversation could not be created. Please try again.")
                print(f"Conversation creation error: {exc}")


def show_messages(conversation, password):
    count = get_message_count(conversation["id"])
    max_messages = int(conversation.get("max_messages") or 10)
    st.caption(f"Messages: {count}/{max_messages}")
    
    expires_at = datetime.fromisoformat(conversation["expires_at"])
    remaining = expires_at - datetime.now(timezone.utc)
    hours = max(0, int(remaining.total_seconds() // 3600))

    st.caption(f"🌸 Expires in {hours}h")

    conversation_status(conversation)
    messages = get_conversation_messages(conversation, password)
    if not messages:
        st.info("No messages yet.")
    for message in messages:
        with st.chat_message("user"):
            st.markdown(f"**{message['sender']}**")
            st.write(message["content"])


def show_chat():
    public_token = params.get("chat", "")
    conversation = get_by_public_token(public_token)
    if not conversation:
        st.error("Conversation not found.")
        return

    authenticated = get_authenticated_conversations()
    authentication = authenticated.get(f"recipient:{public_token}")

    if not authentication:
        st.subheader("Unlock the conversation")
        if conversation["status"] == "expired":
            conversation_status(conversation)
            return
        password = st.text_input("Conversation password", type="password")
        if st.button("Unlock 🌷"):
            if not password:
                st.warning("Enter the conversation password.")
            else:
                success, message, updated = authenticate_recipient(
                    public_token, password
                )
                if success:
                    authenticated[f"recipient:{public_token}"] = {
                        "role": "recipient",
                        "public_token": public_token,
                        "password": password,
                        "conversation_id": conversation["id"],
                    }
                    st.rerun()
                elif message == "locked":
                    st.error("🔒 Too many failed attempts. Access is locked for 15 minutes.")
                elif message == "expired":
                    st.error("🪴 Conversation Expired\n\nThis conversation has expired.")
                elif message == "closed":
                    st.error("🌸 Conversation Ended\n\nMaximum messages reached.")
                else:
                    st.error(message)
        return

    start_chat_autorefresh()
    password = authentication["password"]
    conversation = get_by_public_token(public_token)
    show_messages(conversation, password)

    if conversation["status"] == "active":
        reply = st.chat_input("Reply as 🌷 Tulip")
        if reply:
            if not is_safe(reply):
                st.error("This reply might cross our usage boundaries.")
            else:
                sent, message = send_conversation_reply(
                    conversation, "recipient", reply, password
                )
                if sent:
                    st.rerun()
                else:
                    st.error(message)


def show_manage():
    creator_token = params.get("manage", "")
    conversation = get_by_creator_token(creator_token)
    if not conversation:
        st.error("Access denied. Invalid creator management token.")
        return

    authenticated = get_authenticated_conversations()
    authentication = authenticated.get(f"creator:{creator_token}")
    password = authentication["password"] if authentication else None

    if not password:
        st.subheader("Creator Conversation")
        
        expires_at = datetime.fromisoformat(conversation["expires_at"])
        remaining = expires_at - datetime.now(timezone.utc)
        hours = max(0, int(remaining.total_seconds() // 3600))
        st.caption(f"🌸 Expires in {hours}h")
        
        conversation_status(conversation)
        st.info("Enter the conversation password to view decrypted messages.")
        password = st.text_input("Conversation password", type="password")
        if st.button("Unlock Creator View 🔐"):
            if not password:
                st.warning("Enter the conversation password.")
            else:
                success, message, updated = authenticate_creator(
                    creator_token, password
                )
                if success:
                    authenticated[f"creator:{creator_token}"] = {
                        "role": "creator",
                        "creator_token": creator_token,
                        "public_token": conversation["public_token"],
                        "password": password,
                        "conversation_id": conversation["id"],
                    }
                    st.rerun()
                else:
                    st.error(message)
        return

    start_chat_autorefresh()
    st.subheader("Creator Conversation")
    st.markdown("**Your identity:** 🌹 Rose")
    recipient_link = f"{get_base_url()}?chat={conversation['public_token']}"
    st.markdown("**Recipient link:**")
    st.code(recipient_link)
    show_messages(conversation, password)

    if conversation["status"] == "active":
        reply = st.chat_input("Reply as 🌹 Rose")
        if reply:
            if not is_safe(reply):
                st.error("This reply might cross our usage boundaries.")
            else:
                sent, message = send_conversation_reply(
                    conversation, "creator", reply, password
                )
                if sent:
                    st.rerun()
                else:
                    st.error(message)


if "chat" in params:
    show_chat()
elif "manage" in params:
    show_manage()
else:
    show_home()


page_footer()