import re
import streamlit as st
from engine.manager import supabase
from datetime import datetime, timedelta

FLAGGED_KEYWORDS = [
    # English – abuse / harassment
    "abuse", "harass", "harassment", "threat", "threaten",
    "blackmail", "coerce", "force", "stalk", "stalking",
    "kill", "die", "death", "hurt", "harm",
    "rape", "molest", "assault", "exploit",
    "nude", "naked", "porn", "explicit",
    "slut", "whore", "bitch", "bastard",
    "creep", "pervert", "loser", "idiot",

    # Hindi / Hinglish – gaali / threats
    "maar", "mar dunga", "jaan se", "dhakka", "bsdk", "mc", "bc",
    "madarchod", "blackmail", "zabardasti",
    "chii", "behnchod", "lavde",
    "harami", "kameena", "kutte", "pagal",
    "chutiya", "bakwas", "ghatiya",
    "izzat", "badnaam", "sharminda"
]

def is_safe(text):
    """Returns True if text is safe, False if flagged words found."""
    if not text:
        return True
    
    # Normalize: lowercase and remove punctuation/extra whitespace
    clean_text = re.sub(r'[^\w\s]', '', text.lower())
    words = clean_text.split()

    for word in FLAGGED_KEYWORDS:
        # Check for whole words or phrases in the text
        if word in clean_text:
            return False
    return True

def get_remote_ip():
    """Retrieves the user's IP address from headers."""
    try:
        headers = st.context.headers
        if "X-Forwarded-For" in headers:
            return headers["X-Forwarded-For"].split(",")[0]
        return "127.0.0.1"
    except Exception: return "unknown"

def check_rate_limit(ip):
    """Returns True if IP is under the limit (3 blushes per 6 hours)."""
    six_hours = (datetime.now() - timedelta(hours=6)).isoformat()

    try:
        response = supabase.table("blushes")\
            .select("id", count="exact")\
            .eq("creator_ip", ip)\
            .gte("created_at", six_hours)\
            .execute()
        
        count = response.count if response.count is not None else 0
        return count < 3
    except Exception:
        return True

def is_ip_blocked(ip):
    """Checks if the IP is in our blocklist."""

    try:
        res = supabase.table("blocked_ips").select("ip").eq("ip", ip).execute()
        return len(res.data) > 0
    except Exception:
        return False

def creation_clearance(ip):
    """Final check: Not blocked, under rate limit."""
    if is_ip_blocked(ip):
        return False, "🚫 Your access has been restricted due to policy violations."
    
    if not check_rate_limit(ip):
        return False, "🚦 Limit reached: 3 Blushes per 6 hours. Please wait."
    
    return True, ""