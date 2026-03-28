import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os

# TMDB API KEY
API_KEY = "8536c919ac2517e129f0c3051e787693"
import gdown

# Download similarity.pkl if not present
if not os.path.exists("artifacts/similarity.pkl"):
    url = "https://drive.google.com/uc?id=1OYn0DPYnBFBgnzrczSDLp6hbQ8MLRnQr"
    gdown.download(url, "artifacts/similarity.pkl", quiet=False)

# Load movie data
movies_dict = pickle.load(open('artifacts/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

# Load similarity matrix
similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))


# Function to fetch movie poster
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}&language=en-US"

    try:
        response = requests.get(url, timeout=10)
        data = response.json()

        poster_path = data.get('poster_path')

        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image"

    except requests.exceptions.RequestException as e:
        print("API Error:", e)
        return "https://via.placeholder.com/500x750?text=Error"


# Recommendation function
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies_name = []
    recommended_movies_poster = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies_name.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))

        time.sleep(0.2)  # avoid API rate limit

    return recommended_movies_name, recommended_movies_poster


# Streamlit UI
st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])