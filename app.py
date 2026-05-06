import streamlit as st
from datetime import datetime
import uuid

# 1. Page Configuration & Owner Branding
st.set_page_config(
    page_title="Stars of Undecided Letters", 
    page_icon="✨", 
    layout="centered"
)

# Magic chime sound effect (3-second limit)
star_sound_url = "https://www.soundjay.com/magic/magic-chime-01.mp3"

st.markdown(f"""
    <style>
    .stApp {{ background: radial-gradient(circle at center, #0b0d17 0%, #050505 100%); color: #e0e0e0; }}
    .owner-branding {{ 
        font-family: 'Courier New', monospace; font-size: 16px; text-align: center; 
        color: #FFD700; font-weight: bold; letter-spacing: 3px; text-transform: uppercase; 
    }}
    .main-title {{ 
        font-family: 'Courier New', monospace; font-size: 38px; text-align: center; 
        color: #ffffff; text-shadow: 0 0 15px rgba(255,255,255,0.4); margin-top: -10px; 
    }}
    .stButton>button {{ 
        background: transparent; color: #FFD700; border: 1px solid #FFD700; 
        border-radius: 50%; width: 65px; height: 65px; font-size: 25px; transition: 0.3s; 
    }}
    .stButton>button:hover {{ box-shadow: 0 0 20px #FFD700; background: #FFD700; color: #000; }}
    .letter-box {{ 
        background: rgba(255,255,255,0.05); padding: 25px; border-radius: 15px; 
        border: 1px solid rgba(255,215,0,0.3); backdrop-filter: blur(10px); 
    }}
    </style>
    
    <script>
    function playStarSound() {{
        var audio = new Audio('{star_sound_url}');
        audio.volume = 0.4;
        audio.play();
        setTimeout(function() {{
            audio.pause();
        }}, 3000);
    }}
    </script>
    """, unsafe_allow_html=True)

# Function for Spotify Search Embed (With Scrubber)
def spotify_player(song_query):
    if song_query and song_query.strip():
        search_url = f"https://open.spotify.com/embed/search/{song_query.replace(' ', '%20')}"
        return f"""
        <div style="margin-top: 15px;">
            <iframe src="{search_url}" width="100%" height="152" frameBorder="0" 
            allowfullscreen="" allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture" 
            style="border-radius:12px; box-shadow: 0 0 10px rgba(255,215,0,0.2);"></iframe>
        </div>
        """
    return ""

# Initialize Database
if 'undecided_letters' not in st.session_state:
    st.session_state.undecided_letters = []

query_params = st.query_params
msg_id = query_params.get("id", "")

# --- HEADER ---
st.markdown('<p class="owner-branding">MICHAELA PETITE S. MALABANAN</p>', unsafe_allow_html=True)
st.markdown('<h1 class="main-title">Stars of Undecided Letters</h1>', unsafe_allow_html=True)

# --- RECIPIENT VIEW ---
if msg_id:
    found = next((m for m in st.session_state.undecided_letters if m['id'] == msg_id), None)
    if found:
        st.write("<p style='text-align: center; opacity: 0.7;'>A star and its melody have found you.</p>", unsafe_allow_html=True)
        col1, col2, col3 = st.columns([1,1,1])
        with col2:
            if st.button("⭐", key="direct"):
                st.components.v1.html(f"""<script>window.parent.playStarSound();</script>""", height=0)
                st.session_state.show_direct = True
        
        if st.session_state.get("show_direct", False):
            st.markdown(f"""<div class="letter-box">
                <small style='color:gray;'>{found['time']}</small>
                <p style='font-family:Courier New; font-size:18px; margin-top:10px;'>{found['content']}</p>
                <p style='text-align:right; color:#FFD700; font-size:12px;'>— For: {found['to'].upper()}</p>
            </div>""", unsafe_allow_html=True)
            if found.get("song"):
                st.markdown(spotify_player(found["song"]), unsafe_allow_html=True)

# --- MAIN NAVIGATION ---
else:
    tab1, tab2 = st.tabs(["🔍 Search Sky", "✍️ Leave Letter"])

    with tab1:
        search_name = st.text_input("Whose star are you seeking?", placeholder="Enter name...")
        if search_name:
            query = search_name.lower().strip()
            results = [m for m in st.session_state.undecided_letters if m['to'] == query]
            if results:
                st.write(f"✨ Found {len(results)} star(s):")
                cols = st.columns(5)
                for i, res in enumerate(results):
                    with cols[i % 5]:
                        label = "⭐🎵" if res.get("song") else "⭐"
                        if st.button(label, key=f"s_{i}"):
                            st.components.v1.html(f"""<script>window.parent.playStarSound();</script>""", height=0)
                            st.session_state[f"reveal_{i}"] = True
                    
                    if st.session_state.get(f"reveal_{i}", False):
                        st.markdown(f'<div class="letter-box"><p>{res["content"]}</p></div>', unsafe_allow_html=True)
                        if res.get("song"):
                            st.markdown(spotify_player(res["song"]), unsafe_allow_html=True)

    with tab2:
        with st.form("letter_form", clear_on_submit=True):
            to_name = st.text_input("To:", placeholder="Recipient's Name")
            message = st.text_area("Message:", placeholder="Things left unsaid...")
            
            st.write("🎵 **Search for any Melody**")
            
            # The Aziz Hedra example is set as the placeholder here
            user_song_search = st.text_input(
                "Type Song Title & Artist", 
                placeholder="e.g. Somebody's Pleasure - Aziz Hedra"
            )
            
            if user_song_search.strip():
                st.markdown("**Previewing Match:**")
                st.markdown(spotify_player(user_song_search), unsafe_allow_html=True)
            
            if st.form_submit_button("Release to the Sky"):
                if to_name and message:
                    uid = str(uuid.uuid4())[:8]
                    st.session_state.undecided_letters.append({
                        "id": uid, 
                        "to": to_name.lower().strip(), 
                        "content": message, 
                        "song": user_song_search, 
                        "time": datetime.now().strftime("%d %b %Y").upper()
                    })
                    st.success("Released! Share this star's link:")
                    st.code(f"https://stars-of-undecided-letters.streamlit.app/?id={uid}")

# --- FOOTER ---
st.markdown("<br><hr style='opacity:0.1;'>", unsafe_allow_html=True)
st.markdown(f"<p style='text-align:center; font-size:13px; letter-spacing:1px; color:#FFD700;'>BY MICHAELA PETITE S. MALABANAN</p>", unsafe_allow_html=True)