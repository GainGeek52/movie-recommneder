import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# --- Custom CSS for cinematic aesthetic ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    * {
        font-family: 'Montserrat', sans-serif;
    }
    
    .main {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        color: #FFFFFF;
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 0.8rem 2rem;
        font-size: 1rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px 0 rgba(229, 66, 10, 0.3);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: linear-gradient(90deg, #FF4B2B 0%, #FF416C 100%);
        transform: scale(1.05);
        box-shadow: 0 6px 20px 0 rgba(229, 66, 10, 0.5);
    }
    
    .stSelectbox > div > div {
        background-color: rgba(255, 255, 255, 0.1);
        color: white;
        border-radius: 10px;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    .stSelectbox label {
        color: white;
        font-weight: 600;
    }
    
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
    }
    
    .stSlider > div > div > div > div {
        background: white;
    }
    
    .stSlider label {
        color: white;
        font-weight: 600;
    }
    
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 15px;
        padding: 1rem;
        margin-bottom: 1.5rem;
        box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.2);
        transition: transform 0.3s ease, box-shadow 0.3s ease;
        border: 1px solid rgba(255, 255, 255, 0.1);
        height: 100%;
    }
    
    .movie-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 12px 20px 0 rgba(0, 0, 0, 0.3);
        background: rgba(255, 255, 255, 0.08);
    }
    
    .movie-title {
        font-weight: 700;
        font-size: 1rem;
        margin-top: 0.8rem;
        color: white;
        text-align: center;
        height: 2.8rem;
        overflow: hidden;
        display: -webkit-box;
        -webkit-line-clamp: 2;
        -webkit-box-orient: vertical;
    }
    
    .header {
        text-align: center;
        margin-bottom: 2.5rem;
    }
    
    .header h1 {
        font-weight: 700;
        font-size: 2.8rem;
        background: linear-gradient(90deg, #FF416C 0%, #FF4B2B 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .header p {
        color: rgba(255, 255, 255, 0.7);
        font-size: 1.1rem;
        margin-top: 0;
    }
    
    .recommendation-section {
        margin-top: 2rem;
    }
    
    .recommendation-header {
        font-weight: 600;
        font-size: 1.4rem;
        margin-bottom: 1.5rem;
        color: white;
        text-align: center;
        background: rgba(255, 255, 255, 0.05);
        padding: 0.8rem;
        border-radius: 10px;
    }
    
    div[data-testid="stHorizontalBlock"] {
        align-items: stretch;
    }
    
    /* Custom placeholder for missing posters */
    .placeholder-poster {
        background: linear-gradient(135deg, #2C5364 0%, #203A43 100%);
        border-radius: 10px;
        height: 270px;
        display: flex;
        align-items: center;
        justify-content: center;
        color: rgba(255, 255, 255, 0.5);
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# 🔹 Helper: download file if missing
def download_file(file_id, output):
    if not os.path.exists(output):
        with st.spinner(f"Downloading {output} ..."):
            gdown.download(f"https://drive.google.com/uc?id={file_id}", output, quiet=False)

# 🔹 Download required files
download_file("1O0SheM_jLssJSRJFWp1O0pdTes7svgGA", "similarity.pkl")  # <-- your similarity.pkl file
download_file("YOUR_MOVIE_DICT_FILE_ID", "movie_dict.pkl")            # <-- add movie_dict.pkl file ID here

# 🔹 Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔹 Fetch poster from OMDb
def fetch_poster(movie_title):
    api_key = "a98f5a39"  # <-- your OMDb API key
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={api_key}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        poster_url = data.get("Poster")
        if poster_url and poster_url != "N/A":
            return poster_url
    return None

# 🔹 Recommend movies
def recommend(movie, num_recommendations=5):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# 🔹 Streamlit UI
st.markdown('<div class="header"><h1>🎬 CineMatch</h1><p>Discover your next favorite movie</p></div>', unsafe_allow_html=True)

selected_movie_name = st.selectbox("🎥 Select a movie you enjoy", movies['title'].values)

# Let user choose number of recommendations
num_recs = st.slider("📌 Number of recommendations", min_value=1, max_value=10, value=5)

if st.button("Find Similar Movies"):
    with st.spinner('Searching for the perfect recommendations...'):
        recommendations = recommend(selected_movie_name, num_recs)
        
        st.markdown('<div class="recommendation-section">', unsafe_allow_html=True)
        st.markdown(f'<div class="recommendation-header">Movies similar to "{selected_movie_name}"</div>', unsafe_allow_html=True)
        
        # Display in responsive columns
        cols = st.columns(3)
        for idx, movie in enumerate(recommendations):
            poster = fetch_poster(movie)
            with cols[idx % 3]:
                st.markdown('<div class="movie-card">', unsafe_allow_html=True)
                if poster:
                    st.image(poster, use_column_width=True)
                else:
                    st.markdown(f'<div class="placeholder-poster">🎬 {movie[:15]}...</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="movie-title">{movie}</div>', unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)