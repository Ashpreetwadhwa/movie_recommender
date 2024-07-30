import pickle
import pandas as pd
import streamlit as st
import requests

# Function to fetch poster
def fetch_poster(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
        data = requests.get(url).json()
        poster_path = data.get('poster_path')
        if poster_path:
            full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
            return full_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Image+Available"
    except Exception as e:
        st.error(f"Error fetching poster: {e}")
        return "https://via.placeholder.com/500x750?text=Error+Fetching+Image"

# Function to recommend movies
def recommend(movie):
    try:
        # Debugging: Print the input movie title
        st.write(f"Selected movie: {movie}")

        # Find the index of the selected movie
        index = movies[movies['title'] == movie].index[0]

        # Debugging: Print the index of the selected movie
        st.write(f"Index of selected movie: {index}")

        # Calculate similarity distances
        distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])

        # Debugging: Print the calculated distances
        st.write(f"Similarity distances: {distances[:5]}")

        recommended_movie_names = []
        recommended_movie_posters = []

        for i in distances[1:6]:  # Skip the first index as it is the movie itself
            movie_id = i[0]  # Use .get to avoid KeyError

            # Debugging: Print the movie ID
            st.write(f"Movie ID: {movie_id}")

            if pd.notna(movie_id):  # Check if movie_id is not NaN
                recommended_movie_posters.append(fetch_poster(movie_id))
                recommended_movie_names.append(movies.iloc[i[0]].get('title', 'Unknown Title'))
            else:
                recommended_movie_names.append('Unknown Title')
                recommended_movie_posters.append("https://via.placeholder.com/500x750?text=No+Image+Available")

        # Debugging: Print the recommended movie names and posters
        st.write(f"Recommended movie names: {recommended_movie_names}")
        st.write(f"Recommended movie posters: {recommended_movie_posters}")

        return recommended_movie_names, recommended_movie_posters
    except Exception as e:
        st.error(f"Error generating recommendations: {e}")
        return [], []

# Streamlit UI
st.header('Movie Recommender System')

# Load data
with open('movies_dict.pkl', 'rb') as f:
    movies_dict = pickle.load(f)
    movies = pd.DataFrame(movies_dict)

with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Extract movie titles and convert to list
movie_list = movies['title']  # Convert to list
listt=[]
for i in movie_list:
    listt.append(i)
# Create a selectbox for selecting a movie
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    listt,index=None
)

if st.button('Show Recommendation'):
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

