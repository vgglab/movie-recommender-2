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
  movies_links = []

  for j in sorted_movie_list:
    title = new_df.iloc[j[0]]['title']
    movies_list.append(title)
    response = requests.get(
      f"http://www.omdbapi.com/?apikey=e26fec9f&t={title}"
    )
    json_data = response.json()

    poster = json_data.get('Poster')
    link = 'https://www.imdb.com/title/' + json_data.get('imdbID')

    if poster and poster != "N/A":
      posters_list.append(poster)
      movies_links.append(link)
    else:
      posters_list.append(
        "https://via.placeholder.com/300x450?text=No+Poster"
      )
      movies_links.append(link)

  return movies_list, movies_links, posters_list

def clickable_image(img_url, imdb_url, title):
  return f"""<a href="{imdb_url}" target="_blank"><img src="{img_url}" alt="{title}" width="140"/></a>"""

st.title('Movie Recommendation System')
selected = st.selectbox('Select your favorite movie!', new_df['title'])

if st.button('Recommend'):
    start_time = time.time()
    movies_list, movies_links, posters_list = recommender(selected)
    stop_time = time.time()
    st.write('It took {} seconds!'.format(stop_time - start_time))
    st.header('Your friend is the best movie recommendation system :) althought here is some result')
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.markdown(clickable_image(posters_list[0], movies_links[0], movies_list[0]),
                    unsafe_allow_html=True)
        st.caption(movies_list[0])
    
    with col2:
        st.markdown(clickable_image(posters_list[1], movies_links[1], movies_list[1]),
                    unsafe_allow_html=True)
        st.caption(movies_list[1])
    
    with col3:
        st.markdown(clickable_image(posters_list[2], movies_links[2], movies_list[2]),
                    unsafe_allow_html=True)
        st.caption(movies_list[2])
    
    with col4:
        st.markdown(clickable_image(posters_list[3], movies_links[3], movies_list[3]),
                    unsafe_allow_html=True)
        st.caption(movies_list[3])
    
    with col5:
        st.markdown(clickable_image(posters_list[4], movies_links[4], movies_list[4]),
                    unsafe_allow_html=True)
        st.caption(movies_list[4])

