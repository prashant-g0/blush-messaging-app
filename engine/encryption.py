import base64
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