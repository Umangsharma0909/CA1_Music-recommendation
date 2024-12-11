import streamlit as st
import pandas as pd

# Load the dataset
@st.cache
def load_data():
    data = pd.read_csv('song_dataset.csv')
    data = data[['user', 'title', 'artist_name']].drop_duplicates()
    return data

data = load_data()

# Recommendation function
def recommend_popular_unheard_songs(user_id, top_n=5):
    listened_songs = data[data['user'] == user_id]['title'].unique()
    song_popularity = (
        data.groupby(['title', 'artist_name'])['user']
        .nunique()
        .reset_index()
        .rename(columns={'user': 'unique_user_count'})
    )
    unheard_songs = song_popularity[~song_popularity['title'].isin(listened_songs)]
    recommendations = unheard_songs.sort_values(by='unique_user_count', ascending=False).head(top_n)
    
    if recommendations.empty:
        return f"No popular unheard songs available for user: {user_id}"
    
    return recommendations

# Streamlit App Layout
st.title("🎵 Music Recommendation System")

st.write("""
    Enter your User ID and select the songs you have already listened to.
    We'll recommend new songs you might enjoy!
""")

# User input
user_id_input = st.text_input("Enter your User ID:", "")

# Song selection
unique_songs = sorted(data['title'].unique())
selected_songs = st.multiselect(
    "Select songs you have listened to:",
    options=unique_songs,
    help="Hold down the Ctrl (windows) or Cmd (Mac) button to select multiple options."
)

# Generate recommendations
if st.button("Get Recommendations"):
    if user_id_input:
        recommendations = recommend_popular_unheard_songs(user_id_input, top_n=10)
        if isinstance(recommendations, pd.DataFrame):
            st.table(recommendations.rename(columns={
                'title': 'Song Title',
                'artist_name': 'Artist',
                'unique_user_count': 'Popularity (Unique Listeners)'
            }))
        else:
            st.warning(recommendations)
    else:
        st.error("Please enter a valid User ID.")
