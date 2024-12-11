import streamlit as st
import pandas as pd
import requests

# =====================================
# Load Data
# =====================================
data = pd.read_csv('song_dataset.csv')
data = data[['user', 'title', 'artist_name']].drop_duplicates()

# =====================================
# Recommendation Logic
# =====================================
def recommend_unheard_songs(user_id, top_n=5):
    # Get songs the user has listened to
    listened_songs = data[data['user'] == user_id]['title'].unique()
    # Filter out songs the user has listened to
    unheard_songs = data[~data['title'].isin(listened_songs)]
    
    if unheard_songs.empty:
        return None
    
    # Return top N unheard songs
    recommendations = unheard_songs[['title', 'artist_name']].drop_duplicates().head(top_n)
    return recommendations

# =====================================
# Page Configuration
# =====================================
st.set_page_config(page_title="Dynamic Song Recommendation", page_icon="🎵", layout="wide")

# =====================================
# Custom CSS & Styling
# =====================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
    }

    body {
        background: linear-gradient(to right, #191414, #2e2e2e);
        color: #FFFFFF;
    }

    .stDataFrame table {
        background-color: rgba(0,0,0,0.6);
    }

    .stDataFrame td, .stDataFrame th {
        color: #fff;
    }

    .stDataFrame thead tr th {
        color: #1DB954 !important;
    }

    .stButton>button {
        background-color: #1DB954;
        color: #FFFFFF;
        border: none;
        border-radius: 25px;
        padding: 0.6rem 1.5rem;
        font-size: 1rem;
        font-weight: 700;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        background-color: #1ed760;
        cursor: pointer;
    }

    input[type="text"], input[type="number"] {
        background-color: #333;
        border: 1px solid #444;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# =====================================
# Sidebar
# =====================================
st.sidebar.title("About")
st.sidebar.write("""
This dynamic recommendation engine allows you to:
- Input your **User ID**
- Specify the **Number of Recommendations**

**Instructions:**
1. Enter a valid User ID.
2. Choose how many recommendations you'd like.
3. Click **Get Recommendations**.

Use the **Play Background Music** button below to show the audio player, then press the play button on the player to start music. Automatic play may be blocked by your browser until you interact.

**Data Disclaimer:**
- Recommendations are based on the given dataset.
- If no unheard songs are available, a message will appear.
""")

# =====================================
# Lottie Animation
# =====================================
lottie_url = "https://assets1.lottiefiles.com/packages/lf20_8QvMNs.json"

def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

lottie_animation = load_lottieurl(lottie_url)

if lottie_animation:
    st.lottie(lottie_animation, height=200, key="music_animation")

# =====================================
# Main Section
# =====================================
st.title("Personalized Song Recommendations")
st.markdown("Get new song suggestions based on what you haven't heard yet!")

col1, col2 = st.columns(2)

with col1:
    user_id = st.text_input("Enter your User ID:")
with col2:
    top_n = st.number_input("Number of recommendations:", min_value=1, max_value=50, value=5)

# Button to show the audio player
if st.button("Play Background Music"):
    # Show the audio player
    st.markdown("""
        <audio controls style="width:100%; outline:none;">
            <source src="background_music.mp3" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
    """, unsafe_allow_html=True)

# Button to get recommendations
if st.button("Get Recommendations"):
    user_id_stripped = user_id.strip()
    if user_id_stripped == "":
        st.warning("Please enter a valid User ID.")
    else:
        recommended_songs = recommend_unheard_songs(user_id_stripped, top_n=top_n)
        if recommended_songs is not None and not recommended_songs.empty:
            st.success(f"Here are your top {top_n} recommendations:")
            st.dataframe(recommended_songs.reset_index(drop=True))
        else:
            st.error(f"No unheard songs available for user: {user_id_stripped}.")

