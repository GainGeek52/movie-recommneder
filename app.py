import streamlit as st
import pickle
import pandas as pd
import requests

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

# 🔹 Load data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# 🔹 Streamlit UI
st.title("🎬 Movie Recommender System")
st.write("Find movies similar to your favorite one!")

selected_movie_name = st.selectbox("🎥 Select a Movie", movies['title'].values)

# Let user choose number of recommendations
num_recs = st.slider("📌 How many recommendations do you want?", min_value=1, max_value=10, value=5)

if st.button("Recommend Movies"):
    recommendations = recommend(selected_movie_name, num_recs)

    # Display in 3-column layout
    cols = st.columns(3)
    for idx, movie in enumerate(recommendations):
        poster = fetch_poster(movie)
        with cols[idx % 3]:
            st.image(poster if poster else "https://via.placeholder.com/200x300?text=No+Poster", width=180)
            st.markdown(f"**{movie}**")
