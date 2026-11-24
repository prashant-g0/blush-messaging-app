import hashlib
import os
import secrets
from datetime import datetime, timedelta, timezone

from engine.encryption import (
    decrypt_conversation_text,
    encrypt_conversation_text,
)
from engine.manager import supabase

MAX_MESSAGES = 10
MAX_FAILED_ATTEMPTS = 5
LOCK_DURATION = timedelta(minutes=15)


def get_tokens(type: str) -> str:
    if type == "public":
        return secrets.token_urlsafe(24)
    if type == "creator":
        return secrets.token_urlsafe(32)
    raise ValueError("Unknown token type")


def get_flower() -> dict:
    return {"creator": "🌹 Rose", "recipient": "🌷 Tulip"}


def hash_password(password: str) -> str:
    salt = os.urandom(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 300000)
    return "pbkdf2_sha256$300000$" + base64_url(salt) + "$" + base64_url(digest)


def base64_url(value: bytes) -> str:
    import base64
    return base64.urlsafe_b64encode(value).decode("ascii")


def verify_password(password: str, password_hash: str) -> bool:
    try:
        scheme, iterations, salt_text, digest_text = password_hash.split("$", 3)
        if scheme != "pbkdf2_sha256":
            return False
        import base64
        salt = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        expected = base64.urlsafe_b64decode(digest_text.encode("ascii"))
        actual = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            salt,
            int(iterations),
        )
        return secrets.compare_digest(actual, expected)
    except Exception:
        return False


def _now():
    return datetime.now(timezone.utc)


def _parse_time(value):
    if not value:
        return None
    try:
        parsed = datetime.fromisoformat(str(value).replace("Z", "+00:00"))
        if parsed.tzinfo is None:
            parsed = parsed.replace(tzinfo=timezone.utc)
        return parsed
    except Exception:
        return None


def refresh_conversation_state(conversation):
    if not conversation:
        return conversation

    expires_at = _parse_time(conversation.get("expires_at"))
    if expires_at and expires_at <= _now() and conversation.get("status") != "expired":
        supabase.table("conversations").update({"status": "expired"}).eq(
            "id", conversation["id"]
        ).execute()
        conversation["status"] = "expired"
    return conversation


def create_conversation(initial_message: str, password: str):
    if not initial_message or not password:
        raise ValueError("Initial message and password are required")

    public_token = get_tokens("public")
    creator_token = get_tokens("creator")
    flowers = get_flower()
    expires_at = (_now() + timedelta(hours=24)).isoformat()

    conversation_data = {
        "public_token": public_token,
        "creator_token": creator_token,
        "password_hash": hash_password(password),
        "creator_flower": flowers["creator"],
        "recipient_flower": flowers["recipient"],
        "failed_attempts": 0,
        "locked_until": None,
        "status": "active",
        "max_messages": MAX_MESSAGES,
        "expires_at": expires_at,
    }

    result = supabase.table("conversations").insert(conversation_data).execute()
    if not result.data:
        raise RuntimeError("Could not create conversation")

    conversation = result.data[0]
    encrypted_message = encrypt_conversation_text(initial_message, password)
    supabase.table("conversation_messages").insert({
        "conversation_id": conversation["id"],
        "sender_type": "creator",
        "encrypted_content": encrypted_message,
    }).execute()

    return {
        "id": conversation["id"],
        "public_token": public_token,
        "creator_token": creator_token,
        "expires_at": expires_at,
    }


def get_by_public_token(public_token: str):
    result = (
        supabase.table("conversations")
        .select("*")
        .eq("public_token", public_token)
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    return refresh_conversation_state(result.data[0])


def get_by_creator_token(creator_token: str):
    result = (
        supabase.table("conversations")
        .select("*")
        .eq("creator_token", creator_token)
        .limit(1)
        .execute()
    )
    if not result.data:
        return None
    return refresh_conversation_state(result.data[0])


def authenticate_recipient(public_token: str, password: str):
    conversation = get_by_public_token(public_token)
    if not conversation:
        return False, "Conversation not found.", None

    if conversation["status"] == "expired":
        return False, "expired", conversation

    locked_until = _parse_time(conversation.get("locked_until"))
    if locked_until and locked_until > _now():
        return False, "locked", conversation

    if verify_password(password, conversation["password_hash"]):
        supabase.table("conversations").update({
            "failed_attempts": 0,
            "locked_until": None,
        }).eq("id", conversation["id"]).execute()
        return True, "authenticated", conversation

    failed_attempts = int(conversation.get("failed_attempts") or 0) + 1
    update = {"failed_attempts": failed_attempts}
    if failed_attempts >= MAX_FAILED_ATTEMPTS:
        update["locked_until"] = (_now() + LOCK_DURATION).isoformat()
        result_message = "locked"
    else:
        result_message = "Incorrect password."
    supabase.table("conversations").update(update).eq(
        "id", conversation["id"]
    ).execute()
    return False, result_message, conversation


def authenticate_creator(creator_token: str, password: str):
    conversation = get_by_creator_token(creator_token)
    if not conversation:
        return False, "Conversation not found.", None

    if verify_password(password, conversation["password_hash"]):
        return True, "authenticated", conversation
    return False, "Incorrect conversation password.", conversation


def get_message_count(conversation_id: str) -> int:
    result = (
        supabase.table("conversation_messages")
        .select("id", count="exact")
        .eq("conversation_id", conversation_id)
        .execute()
    )
    return result.count if result.count is not None else len(result.data or [])


def get_conversation_messages(conversation, password: str):
    conversation = refresh_conversation_state(conversation)
    result = (
        supabase.table("conversation_messages")
        .select("sender_type, encrypted_content, created_at")
        .eq("conversation_id", conversation["id"])
        .order("created_at", desc=False)
        .execute()
    )

    messages = []
    for message in result.data or []:
        sender_type = message["sender_type"]
        flower = (
            conversation["creator_flower"]
            if sender_type == "creator"
            else conversation["recipient_flower"]
        )
        messages.append({
            "sender": flower,
            "sender_type": sender_type,
            "content": decrypt_conversation_text(
                message["encrypted_content"], password
            ),
            "created_at": message["created_at"],
        })
    return messages


def send_conversation_reply(conversation, sender_type: str, reply_text: str, password: str):
    if sender_type not in ("creator", "recipient"):
        return False, "Invalid sender."

    conversation = refresh_conversation_state(conversation)
    if conversation["status"] == "expired":
        return False, "⏰ Conversation Expired"
    if conversation["status"] != "active":
        return False, "🌸 Conversation Ended"

    if not reply_text or not reply_text.strip():
        return False, "Please enter a message."

    count = get_message_count(conversation["id"])
    if count >= int(conversation.get("max_messages") or MAX_MESSAGES):
        supabase.table("conversations").update({"status": "closed"}).eq(
            "id", conversation["id"]
        ).execute()
        return False, "🌸 Conversation Ended"

    encrypted_reply = encrypt_conversation_text(reply_text.strip(), password)
    supabase.table("conversation_messages").insert({
        "conversation_id": conversation["id"],
        "sender_type": sender_type,
        "encrypted_content": encrypted_reply,
    }).execute()

    new_count = count + 1
    if new_count >= int(conversation.get("max_messages") or MAX_MESSAGES):
        supabase.table("conversations").update({"status": "closed"}).eq(
            "id", conversation["id"]
        ).execute()

    return True, "Message sent."

def get_all_time_conversations():
    result = supabase.table("conversations").select("id", count="exact").execute()
    return result.count if result.count is not None else len(result.data or [])

def get_total_conversations():
    result = (
        supabase.table("conversations")
        .select("id", count="exact")
        .eq("status", "active")
        .execute()
    )
    return result.count if result.count is not None else len(result.data or [])