import streamlit as st
import pickle
import pandas as pd
import requests

# Replace with your TMDB API Key
API_KEY = 'a7bd14802d79d0d26f4226e9fea39089'


def fetch_poster(movie_title):
    # Search for the movie by title to get its ID
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={API_KEY}&query={movie_title}"
    search_response = requests.get(search_url)
    search_data = search_response.json()

    if search_data['results']:
        movie_id = search_data['results'][0]['id']  # Get the first movie result
        poster_path = search_data['results'][0]['poster_path']  # Get the poster path

        if poster_path:
            full_poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"  # Base URL for TMDB images
            return full_poster_url
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Available"
    else:
        return "https://via.placeholder.com/500x750?text=Movie+Not+Found"




def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_title = movies.iloc[i[0]].title  # Fetch movie title
        recommended_movies.append(movie_title)
        recommended_movies_posters.append(fetch_poster(movie_title))  # Use title to fetch poster

    return recommended_movies, recommended_movies_posters


# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

# Movie selection dropdown for regular recommendations
selected_movie_name = st.selectbox(
    'Select a movie for recommendations:',
    movies['title'].values
)

if st.button('Show Regular Recommendations'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.image(recommended_movie_posters[0], caption=recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1], caption=recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2], caption=recommended_movie_names[2])
    with col4:
        st.image(recommended_movie_posters[3], caption=recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4], caption=recommended_movie_names[4])

