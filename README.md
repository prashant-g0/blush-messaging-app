# 🌸 Blush

> **A privacy-first, ephemeral secret vault for messages that deserve to disappear.**
>
> Share encrypted secrets, anonymous confessions, and one-time messages without accounts, tracking, or permanent digital footprints.

[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io)
[![Supabase](https://img.shields.io/badge/Supabase-PostgreSQL-3ECF8E?logo=supabase&logoColor=white)](https://supabase.com)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Privacy First](https://img.shields.io/badge/Privacy-First-success)](#security)
[![Encryption](https://img.shields.io/badge/Encryption-AES--256-important)](#security)

##  Overview

**Blush** is a secure, anonymous, and ephemeral messaging platform built for moments that shouldn't live forever.

Whether you're sending a private password-protected note to someone special or anonymously posting a confession to a community wall, every interaction on Blush is designed around one fundamental principle:

> **Messages should exist only as long as they are needed.**

No accounts. No profiles. No tracking. No permanent archives.

---

## 🌷 Why Blush?

Modern communication platforms are built to remember everything.

Blush is built to forget.

By combining strong encryption, automatic expiration, one-time access controls, and anonymous participation, Blush creates a space where people can share thoughts freely without worrying about long-term digital footprints.

---

##  Features

###  Anonymous Two-Way Conversations

- Password-protected, encrypted creator and recipient conversations
- Private creator management link and shareable recipient link
- Automatic 24-hour expiry and 10-message limit
- Five-failure password lock and read-only closed/expired states

###  Private Blush

Create secure, password-protected notes that:

- Are encrypted before storage
- Can be accessed only once
- Automatically expire after **6 hours**
- Require a secret password to unlock
- Leave no permanent message history

Perfect for:

- Personal secrets
- Private confessions
- Temporary credentials
- Sensitive conversations
- One-time information sharing

---

### Wall of Confessions

An anonymous public space where users can:

- Post confessions anonymously
- Read community submissions
- Express thoughts without identity exposure
- Participate without creating an account

All posts automatically disappear after **7 days**.

---

###  Ephemeral by Design

Every piece of content has a limited lifespan:

| Content Type | Expiration |
|-------------|------------|
| Private Blush | 6 Hours |
| Wall Post | 7 Days |

No manual cleanup required.

---

##  Security

Security is the foundation of Blush.

### Encryption

- AES-256 encryption for sensitive data
- Content encrypted before database storage
- Encryption keys managed through environment variables
- Database contents remain unreadable without valid encryption keys

### Password Protection

- Passwords are hashed using bcrypt
- Plain-text passwords are never stored
- Secure verification during message access

### Privacy Guarantees

✅ No user accounts  
✅ No activity tracking  
✅ No analytics scripts  
✅ No personal profiles  
✅ No permanent message history  
✅ Automatic data deletion

---

##  Tech Stack

| Category | Technology |
|-----------|------------|
| Frontend | Streamlit |
| Backend | Python |
| Database | Supabase (PostgreSQL) |
| Encryption | Cryptography (Fernet / AES-256) |
| Password Hashing | bcrypt |
| Package Management | uv |
| Scheduling | PostgreSQL Cron Jobs |
| Hosting | Streamlit Community Cloud |

---

##  Getting Started

### Prerequisites

- Python 3.13+
- uv
- Supabase Project

### Installation

```bash
git clone https://github.com/prashant-g0/blush-messaging-app.git

cd blush-messaging-app

uv venv

source .venv/bin/activate
# Windows:
# .venv\Scripts\activate

uv sync
```

### Environment Variables

Create a `.env` file:

```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

### Run Locally

```bash
streamlit run app.py
```

Application will be available at:

```text
http://localhost:8501
```

---

## Data Lifecycle

```text
Create Message
       │
       ▼
Encrypt Content
       │
       ▼
Store Securely
       │
       ▼
Read Once (Private Blush)
       │
       ▼
Automatic Expiration
       │
       ▼
Permanent Deletion
```

---

##  Design Principles

Blush follows a simple set of principles:

- Privacy by Default
- Encryption First
- Anonymous Participation
- Minimal Data Collection
- Ephemeral Communication
- Security Over Convenience

---

##  Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch

```bash
git switch -c feature/amazing-feature
```

3. Commit your changes

```bash
git commit -m "Add amazing feature"
```

4. Push your branch

```bash
git push origin feature/amazing-feature
```

5. Open a Pull Request

---

## 📄 License

Distributed under the MIT License.

See `LICENSE` for more information.

---

## Links

- **Live Demo:** https://blushnow.streamlit.app

---

<div align="center">

### 🌸 Blush

**Private. Anonymous. Temporary.**

Made with 💗 by **Prashant Gupta**

</div>