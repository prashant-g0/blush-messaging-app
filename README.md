# 🌸 Blush

### Blush is a minimal, privacy-first web app that lets you send a message meant to be read only once.

**No accounts. | No tracking. | No history.**

#### ✨ What is Blush?

Blush is built for moments that don’t need permanence.
It allows you to create a one-time, encrypted message that can be unlocked only by the intended recipient.

**If replied, it becomes a complete conversation.**

#### 🔐 Core Principles
- One-time access: messages can be opened only once
- End-to-end style encryption: content is encrypted before storage
- No user accounts: complete anonymity
- No tracking or analytics
- Ephemeral by design: messages fade after their purpose is served

#### 🌷 Features

- Create a secure, one-time message
- Password-protected access
- Optional reply cycle (also one-time)
- Automatic locking against multiple readers
- Graceful expiry and archive flow
- Soft, romantic, minimal UI

#### 🛠️ Tech Stack
- Frontend & Backend: Python + Streamlit
- Database: Supabase (PostgreSQL)
- Security:
- - Password hashing (bcrypt)
- - Message encryption (Fernet / AES)
- Hosting: Streamlit Community Cloud

#### 🔒 Security Overview
- Passwords are hashed, never stored in plain text
- Sender name, message, and replies are encrypted before saving
- Encryption keys are stored securely using environment variables
- Even database access alone cannot reveal message contents
- If the database leaks, the messages remain unreadable.

<p style='text-align: center; color:#888;'>2026 | Prashant Gupta | Developed with Blush 💗</p>