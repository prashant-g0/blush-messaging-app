# 🌸 Blush | Your Secure, Ephemeral Secret Vault

**Blush** is a privacy-first web application designed for the moments when words deserve to be felt, but not necessarily stored forever. It bridges the gap between private, encrypted communication and public, community-driven confessions.

**No accounts. | No tracking. | No history.**

## 🌷 The Core Philosophy
In an era of permanent digital footprints, **Blush** offers a space for the "unsaid". Whether it’s a private message for a specific person or an anonymous post on the Wall, everything is designed to fade away—just like a shared secret should.

--- 
## 🛣️ Two Distinct Paths:
1. **Private Blush:** A password-protected, AES-256 encrypted note that vanishes in **6 hours**.
2. **Wall of Confessions:** An anonymous public square for community sharing, where posts vanish after **7 days**.

---

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
- Automation: PostgreSQL Cron Jobs for auto-purging data
- Security: `cryptography` library (AES-256)
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