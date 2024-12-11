import streamlit as st
import pandas as pd
import requests
from streamlit_lottie import st_lottie
import os

# =====================================
# Function to Load Lottie Animations
# =====================================
def load_lottieurl(url: str):
    """
    Load a Lottie animation from a URL.
    """
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# =====================================
# Recommendation Logic
# =====================================
@st.cache_data
def load_data(filepath):
    """
    Load and preprocess the song dataset.
    """
    data = pd.read_csv(filepath)
    data = data[['user', 'title', 'artist_name']].drop_duplicates()
    return data

def recommend_unheard_songs(data, user_id, top_n=5):
    """
    Recommend songs that the user hasn't listened to yet.
    """
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
st.set_page_config(
    page_title="🎵 Personalized Song Recommendations",
    page_icon="🎶",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================
# Custom CSS for Styling
# =====================================
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Montserrat', sans-serif;
        background-color: #121212;
        color: #FFFFFF;
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

    .stTextInput>div>div>input {
        background-color: #333333;
        border: 1px solid #444444;
        color: #FFFFFF;
    }

    .stSlider>div>div>div>div>input {
        background-color: #1DB954;
    }

    .stDataFrame table {
        background-color: rgba(0,0,0,0.8);
        border: none;
    }

    .stDataFrame td, .stDataFrame th {
        color: #FFFFFF;
    }

    .stDataFrame thead tr th {
        color: #1DB954;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================
# Sidebar - About and Instructions
# =====================================
st.sidebar.title("About")
st.sidebar.write("""
### 🎵 Personalized Song Recommendation Engine

This application recommends songs you haven't listened to yet based on your listening history.

**Features:**
- **User Input:** Enter your User ID and select the number of recommendations you desire.
- **Dynamic UI:** Enjoy a modern, Spotify-inspired interface with animations.
- **Background Music:** Immerse yourself with background music that plays automatically.

**Note:** 
- Ensure you have a valid User ID present in the dataset.
- Background music autoplay may be blocked by some browsers. If it doesn't play automatically, try interacting with the page (e.g., clicking a button).
""")

# =====================================
# Load Assets
# =====================================
# Load Lottie Animation
lottie_animation_url = "https://assets1.lottiefiles.com/packages/lf20_8QvMNs.json"  # Replace with your preferred animation URL
lottie_animation = load_lottieurl(lottie_animation_url)

# =====================================
# Load Dataset
# =====================================
data_file = 'song_dataset.csv'
if not os.path.exists(data_file):
    st.error(f"Dataset file `{data_file}` not found. Please ensure it's in the same directory as the app.")
    st.stop()

data = load_data(data_file)

# =====================================
# Layout - Header and Animation
# =====================================
col1, col2 = st.columns([2, 1])

with col1:
    st.title("🎶 Personalized Song Recommendations")
    st.markdown("Get new song suggestions based on what you haven't heard yet!")

with col2:
    if lottie_animation:
        st_lottie(lottie_animation, height=150, key="music_animation")

# =====================================
# Background Music Autoplay
# =====================================
background_music_file = 'background_music.mp3'
if os.path.exists(background_music_file):
    # Attempt to autoplay background music
    # Note: Browsers may block autoplay. Users might need to interact with the page.
    st.markdown(
        f"""
        <audio autoplay loop>
            <source src="data:audio/mp3;base64,{st.secrets['BACKGROUND_MUSIC']}" type="audio/mp3">
            Your browser does not support the audio element.
        </audio>
        """,
        unsafe_allow_html=True
    )
else:
    st.warning(f"Background music file `{background_music_file}` not found. Please ensure it's in the same directory as the app.")

# =====================================
# User Input Section
# =====================================
st.markdown("---")
st.header("Enter Your Details")

col1, col2 = st.columns(2)

with col1:
    user_id = st.text_input("**User ID:**", value="", placeholder="Enter your User ID")

with col2:
    top_n = st.slider("**Number of Recommendations:**", min_value=1, max_value=50, value=5, step=1)

# =====================================
# Recommendation Button
# =====================================
if st.button("Get Recommendations"):
    if user_id.strip() == "":
        st.warning("Please enter a valid User ID.")
    else:
        recommendations = recommend_unheard_songs(data, user_id.strip(), top_n)
        if recommendations is not None and not recommendations.empty:
            st.success("### 🎉 Recommended Songs:")
            st.dataframe(recommendations.reset_index(drop=True))
        else:
            st.error(f"No unheard songs available for user: `{user_id.strip()}`.")

# =====================================
# Footer
# =====================================
st.markdown("---")
st.markdown("""
<center>
    <p>© 2024 Song Recommendation Engine. All rights reserved.</p>
</center>
""", unsafe_allow_html=True)
