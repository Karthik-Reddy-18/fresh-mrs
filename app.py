import streamlit as st
import pickle
import pandas as pd
import requests
import time
import os
import gdown

API_KEY = "8536c919ac2517e129f0c3051e787693"

# ensure folder exists
os.makedirs("artifacts", exist_ok=True)

# download similarity file if missing
if not os.path.exists("artifacts/similarity.pkl"):
    url = "https://drive.google.com/uc?id=1OYn0DPYnBFBgnzrczSDLp6hbQ8MLRnQr"
    gdown.download(url, "artifacts/similarity.pkl", quiet=False)


@st.cache_resource
def load_data():
    movies_dict = pickle.load(open('artifacts/movies_dict.pkl', 'rb'))
    movies = pd.DataFrame(movies_dict)
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
    return movies, similarity


movies, similarity = load_data()

 
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

    except requests.exceptions.RequestException:
        return "https://via.placeholder.com/500x750?text=Error"


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    names = []
    posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        names.append(movies.iloc[i[0]].title)
        posters.append(fetch_poster(movie_id))
        time.sleep(0.2)

    return names, posters


st.title("🎬 Movie Recommender System")

selected_movie = st.selectbox(
    "Select a movie",
    movies['title'].values
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)

    cols = st.columns(5)

    for i in range(5):
        with cols[i]:
            st.text(names[i])
            st.image(posters[i])