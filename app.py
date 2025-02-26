import streamlit as st
import pickle
import pandas as pd
import requests

# function to fetch poster of a movie
def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=a33777f8de7c2bae19f41870405b76ae&language=en-US', timeout=5)
        response.raise_for_status()  # Raise HTTPError for bad responses
        data = response.json()
        return 'https://image.tmdb.org/t/p/w500/' + data['poster_path']
    except requests.exceptions.ConnectionError:
        return 'Movie Recommender System/poster not available.png'
    except requests.exceptions.RequestException as e:
        return 'Movie Recommender System/poster not available.png'


# function to recommend a movie
def recommend(movie):
    movie_loc = movies.index[movies['title']==movie][0]
    similar_movies = similarity[movie_loc]
    similar_movies = sorted(list(enumerate(similar_movies)), reverse=True, key=lambda x:x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title) # fetch movie title
        recommended_movies_posters.append(fetch_poster(movie_id)) # fetch movie poster
    return recommended_movies, recommended_movies_posters

movies_dict = pickle.load(open('Movie Recommender System/movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open('Movie Recommender System/similarity.pkl', 'rb'))

st.title("Movie Recommender System")

selected_movie = st.selectbox(
    "Select a Movie from the Dropdown",
    (movies['title'].values),
)

if st.button("Recommend"):
    names, posters = recommend(selected_movie)
    
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.write(names[0])
        st.image(posters[0])

    with col2:
        st.write(names[1])
        st.image(posters[1])


    with col3:
        st.write(names[2])
        st.image(posters[2])


    with col4:
        st.write(names[3])
        st.image(posters[3])


    with col5:
        st.write(names[4])
        st.image(posters[4])

# Connection Error 10054 apparent reasons - The web server actively rejected your connection. That's usually because it is congested, has rate limiting or thinks that you are launching a denial of service attack.
