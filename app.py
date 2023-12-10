import pickle
import pandas as pd
import streamlit as st
import requests

def fetch_poster(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2e2234e7dd46dd60ccad760c14b82996')
    data = response.json()
    if 'poster_path' in data:
        return f"https://image.tmdb.org/t/p/original{data['poster_path']}"
    else:
        return "https://example.com/default_poster.jpg"

def recommend(movie, movies, similarity, max_recommendations=3):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:max_recommendations + 1]
    recommend_movies = []
    recommend_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fetch_poster(movie_id))
    return recommend_movies, recommend_movies_posters

def open_full_movie(movie_url):
    st.sidebar.write(f'Opening full movie:')
    st.sidebar.write(f'<a href="{movie_url}" target="_blank">Click here ! and Watch movie</a>', unsafe_allow_html=True)

# Load data and similarity
movies_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit app
st.title('Movie Recommender System')

movie_list = movies['title'].values.tolist()
selected_movie_name = st.selectbox(
    'Select a movie:',
    movie_list)

recommend_movies, recommend_movies_posters = recommend(selected_movie_name, movies, similarity, max_recommendations=3)

st.markdown('Recommended movies:')
st.markdown('---')

columns = st.columns(3)

for name, poster, column in zip(recommend_movies, recommend_movies_posters, columns):
    with column:
        st.image(poster, caption=name, width=200)
        youtube_url = "https://www.youtube.com/"# Replace this with the actual YouTube URL for the movie
        st.button(f'Open full movie {name}', on_click=lambda url=youtube_url: open_full_movie(url))

# Show the first 20 movies with images
st.title('YOU ALSO LIKE TO WATCH...')

st.markdown('---')
columns = st.columns(3)
for index, row in movies.head(20).iterrows():
    with columns[index % 3]:
        st.image(fetch_poster(row['movie_id']), caption=row['title'], width=200)
