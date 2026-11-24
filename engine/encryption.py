import base64
import os
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.fernet import Fernet

def get_cipher(password):
    """Derives a deterministic key from the password."""
    salt = b'blush_static_salt_secure'
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=100000,
    )

    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    return Fernet(key)

def encrypt_text(text, password):
    if not text: return ""
    cipher = get_cipher(password)
    return cipher.encrypt(text.encode()).decode()

def decrypt_text(ciphertext, password):
    if not ciphertext: return ""
    try:
        cipher = get_cipher(password)
        return cipher.decrypt(ciphertext.encode()).decode()
    except Exception:
        return "⚠️ Decryption Failed: Data corrupted or wrong password."


def encrypt_conversation_text(text: str, password: str) -> str:
    """Encrypt with a random per-message salt for anonymous conversations."""
    if not text:
        return ""

    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=300000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
    token = Fernet(key).encrypt(text.encode("utf-8"))
    return base64.urlsafe_b64encode(salt).decode("ascii") + "$" + token.decode("ascii")


def decrypt_conversation_text(ciphertext: str, password: str) -> str:
    """Decrypt a conversation value; return a safe UI error for invalid data."""
    if not ciphertext:
        return ""

    try:
        salt_text, token = ciphertext.split("$", 1)
        salt = base64.urlsafe_b64decode(salt_text.encode("ascii"))
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=300000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode("utf-8")))
        return Fernet(key).decrypt(token.encode("ascii")).decode("utf-8")
    except Exception:
        return "⚠️ Unable to decrypt this message."