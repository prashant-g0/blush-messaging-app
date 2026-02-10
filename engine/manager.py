import os
import secrets
import string
import hashlib
from datetime import datetime
from supabase import create_client, Client
from dotenv import load_dotenv

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

def create_blush(name, message, password):
    """Hashes the pssword & insert the new message into supabase."""
    code = code_generator() 
    password_hash = hashlib.sha256(password.encode()).hexdigest() 

    blush_data = {
        "code": code,
        "sender_name": name,
        "message": message,
        "password_hash":password_hash,
        "status": "unread"
    }

    try:
        supabase.table("blushes").insert(blush_data).execute()
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

def submit_reply(code, reply_text):
    """Saves the reply & marks the Blush as replied."""
    data = {
        "reply": reply_text,
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
    
def get_total_blushes():
    """Returns the total number of blushes ever created."""
    try:
        response = supabase.table("blushes").select("*", count="exact").execute()
        return response.count if response.count else 0
    except Exception as e:
        print(f"Error fetching count: {e}")
        return 0