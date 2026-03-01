import os
import secrets
import string
import hashlib
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv
from engine.encryption import encrypt_text

load_dotenv() 
URL = os.getenv("SUPABASE_URL") 
KEY = os.getenv("SUPABASE_KEY")

supabase: Client = create_client(URL, KEY)

def code_generator():
    """Generates a random 6-digit code & verifies it's not already in Supabase."""
    chars = string.ascii_uppercase + string.digits

    while True:
        code = ''.join(secrets.choice(chars) for _ in range(6)) 
        result = supabase.table("blushes").select("code").eq("code", code).execute() 
        
        if not result.data:
            return code

def create_blush(name, message, password, creator_ip):
    """Hashes the pssword & insert the new message into supabase."""
    code = code_generator() 
    password_hash = hashlib.sha256(password.encode()).hexdigest() 
    encrypted_msg = encrypt_text(message, password)

    blush_data = {
        "code": code,
        "sender_name": name,
        "message": encrypted_msg,
        "password_hash":password_hash,
        "status": "unread",
        "creator_ip": creator_ip
    }

    try:
        supabase.table("blushes").insert(blush_data).execute()
        increment_global_count()
        return code
    except Exception as e:
        print(f"Error creating a blush: {e}")
        return None
    
def verify_and_lock(code, input_password):
    """
    Checks credentials & manages state transitions:
    unread -> reading
    replied -> opened
    Handles blocked states: reading, rejected, opened
    """
    response = supabase.table("blushes").select("*").eq("code", code).execute()
    if not response.data:
        return False, "Code not found.", None
    
    blush = response.data[0]
    status = blush['status']

    if status == "reading":
        return False, "Someone is currently reading this, or the session was interrupted.", status
    if status == "rejected":
        return False, "This message was rejected by your partner.", status
    if status == "opened":
        return False, "This code had a good convo, but the love cycle of this message has ended.", status
        
    input_hash = hashlib.sha256(input_password.encode()).hexdigest()
    if input_hash != blush['password_hash']:
        return False, "Incorrect password.", status

    if status == "unread":
        supabase.table("blushes").update({"status": "reading"}).eq("code", code).execute()
        return True, blush, "reading"
    
    if status == "replied":
        supabase.table("blushes").update({"status": "opened"}).eq("code", code).execute()
        return True, blush, "replied"

    return False, "Unexpected error.", status

def submit_reply(code, reply_text, password):
    """Saves the reply & marks the Blush as replied."""

    encrypted_reply = encrypt_text(reply_text, password)
    data = {
        "reply": encrypted_reply,
        "status":"replied",
        "replied_at": datetime.now().isoformat()
    }

    try:
        supabase.table("blushes").update(data).eq("code", code).execute()
        return True
    except Exception as e:
        print(f"Error submitting reply as: {e}")
        return False
    
def reject_blush(code):
    """Updates status to rejected when user declines to reply."""
    try:
        supabase.table("blushes").update({"status": "rejected"}).eq("code", code).execute()
        return True
    except Exception as e:
        print(f"Error rejecting blush: {e}")
        return False


def fetch_result(code):
    """Allow the sender to see if a reply exists."""
    response = supabase.table("blushes").select("status", "reply", "sender_name", "message").eq("code", code).execute()

    if response.data:
        return response.data[0]
    
    return None

def burn_blush(code):
    """Permanently deletes the row from the database."""
    try:
        supabase.table("blushes").delete().eq("code", code).execute()
        return True
    except Exception as e:
        print(f"Error burning blush: {e}")
        return False
    
def increment_global_count():
    """Triggers the atomic database-level increment."""
    try:
        # No logic needed here, just trigger the function
        supabase.rpc("increment_stats").execute()
    except Exception as e:
        print(f"Stats error: {e}")
    
def get_total_blushes():
    """Returns the total number of blushes in db."""
    try:
        response = supabase.table("blushes").select("*", count="exact").execute()
        return response.count if response.count else 0
    except Exception as e:
        print(f"Error fetching count: {e}")
        return 0
    
def get_all_time_count():
    """Fetches the persistent count from the stats table."""
    try:
        res = supabase.table("global_stats").select("total_created").eq("id", 1).single().execute()
        return res.data['total_created'] if res.data else 0
    except Exception:
        return 0
    
def report_blush(code, reporter_ip):
    try:
        response = supabase.table("blushes").select("*").eq("code", code).execute()
        
        if not response.data or len(response.data) == 0:
            print("Report Failed: No blush found with that code.")
            return False
        
        blush = response.data[0]

        report_data = {
            "original_code": str(blush.get('code', '')),
            "sender_name": str(blush.get('sender_name', 'Anonymous')),
            "message_encrypted": str(blush.get('message', '')),
            "sender_ip": str(blush.get('creator_ip', 'unknown')),
            "reporter_ip": str(reporter_ip)
        }
        
        supabase.table("reported_blushes").insert(report_data).execute()
        
        supabase.table("blushes").update({"status": "reported"}).eq("code", code).execute()
        
        return True
    except Exception as e:
        print(f"Report Failed at catch: {e}")
        return False
    
def get_confessions(search_query=None):
    """Fetches confessions, optionally filtered by receiver name."""
    try:
        query = supabase.table("confessions").select("*").order("created_at", desc=True)
        if search_query:
            # Case-insensitive partial match
            query = query.ilike("receiver_name", f"%{search_query}%")
        
        result = query.execute()
        return result.data
    except Exception as e:
        print(f"Error fetching confessions: {e}")
        return []

def create_confession(receiver_name, content, creator_ip):
    """Inserts a new public confession into the database."""
    data = {
        "receiver_name": receiver_name,
        "content": content,
        "creator_ip": creator_ip
    }
    try:
        supabase.table("confessions").insert(data).execute()
        current_all_time = get_all_time_conf()
        supabase.table("global_stats").update({"confessions_total": current_all_time + 1}).eq("id", 1).execute()
        return True
    except Exception as e:
        print(f"Error creating confession: {e}")
        return False
    
def get_total_conf():
    """Returns the count of confessions currently on the wall (Live)."""
    try:
        response = supabase.table("confessions").select("*", count="exact").execute()
        return response.count if response.count is not None else 0
    except Exception as e:
        print(f"Error fetching current confession count: {e}")
        return 0

def get_all_time_conf():
    """Fetches the all time total confessions from the global_stats table"""
    try:
        response = supabase.table("global_stats").select("confessions_total").eq("id", 1).single().execute()
        return response.data["confessions_total"] if response.data else 0
    except Exception as e:
        return 0

