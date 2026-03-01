import streamlit as st
import datetime
from engine.manager import get_confessions, create_confession
from engine.safety import is_safe, get_remote_ip

st.set_page_config(
    page_title="Blush | Confession Wall", 
    page_icon="🕊️",
    layout="wide")

st.title("🕊️ Wall of Confessions")
st.markdown("A public space for the words you've been holding back. Secrets here vanish in 7 days.")

# --- SECTION: Post a Confession ---
with st.expander("📝 Write a Public Confession"):
    c_name = st.text_input("To (Name)", placeholder="e.g. Satvik")
    c_text = st.text_area("Your Confession", placeholder="Write it out...", max_chars=300)
    
    if st.button("Post to Wall", use_container_width=True):
        user_ip = get_remote_ip()
        
        if not c_name or not c_text:
            st.error("Please fill in both fields.")
        elif not is_safe(c_text):
            st.error("Keep it respectful. No inappropriate language allowed.")
        else:
            if create_confession(c_name, c_text, user_ip):
                st.toast("Pinned to the wall! ✨")
                st.rerun()

st.divider()

# --- SECTION: Search & The Wall ---
search = st.text_input("🔍 Search for a name", placeholder="Who are you looking for?")
results = get_confessions(search)

if not results:
    st.info(f"No confessions found for '{search}'. Why not start the conversation?")
else:
    # Masonry-style Grid (3 Columns)
    cols = st.columns(3)
    for idx, item in enumerate(results):
        with cols[idx % 3]:
            with st.container(border=True):
                st.subheader(f"To: {item['receiver_name']}")
                st.write(item['content'])
                
                # Format the creation time
                raw_date = item['created_at'].replace('Z', '+00:00')
                utc_dt = datetime.datetime.fromisoformat(raw_date)

                # Add IST Offset (+05:30)
                ist_offset = datetime.timedelta(hours=5, minutes=30)
                local_date = utc_dt + ist_offset

                st.caption(f"🕒 {local_date.strftime('%b %d, %I:%M %p')}")

st.markdown("<p style='text-align: center; color:#888;'>2026 | Prashant Gupta | Developed with Blush 💗</p>", unsafe_allow_html=True)