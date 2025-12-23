import streamlit as st
import joblib
import requests
import time
from sklearn.metrics.pairwise import cosine_similarity

vectors = joblib.load('vectors.joblib')
new_df = joblib.load('new_df.joblib')
similarity = cosine_similarity(vectors)


def recommender(movie_name: str):
  idx = new_df.index[new_df['title'] == movie_name.strip()][0]

  sorted_movie_list = sorted(
    list(enumerate(similarity[idx])),
    key=lambda x: x[1],
    reverse=True
  )[1:6]

  movies_list = []
  posters_list = []

  for j in sorted_movie_list:
    title = new_df.iloc[j[0]]['title']
    movies_list.append(title)
    response = requests.get(
      f"http://www.omdbapi.com/?apikey=e26fec9f&t={title}"
    )
    json_data = response.json()

    poster = json_data.get('Poster')

    if poster and poster != "N/A":
      posters_list.append(poster)
    else:
      posters_list.append(
        "https://via.placeholder.com/300x450?text=No+Poster"
      )

  return movies_list, posters_list

st.title('Movie Recommender System')
selected = st.selectbox('Select your favorite movie!', new_df['title'])

if st.button('Recommend'):
    st.write('fetching movies for you')
    start_time = time.time()
    movies_list, posters_list = recommender(selected)
    stop_time = time.time()
    st.write('It took {} seconds!'.format(stop_time - start_time))
    st.header('Your friend is best movie recommender system :) althought here is some result')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.image(posters_list[0], caption=movies_list[0], width=140)
    with col2:
        st.image(posters_list[1], caption=movies_list[1], width=140)
    with col3:
        st.image(posters_list[2], caption=movies_list[2], width=140)
    with col4:
        st.image(posters_list[3], caption=movies_list[3], width=140)
    with col5:
        st.image(posters_list[4], caption=movies_list[4], width=140)
