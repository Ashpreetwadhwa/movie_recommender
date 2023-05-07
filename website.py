import requests
from flask import Flask, render_template, request, jsonify
import pickle
import pandas as pd
movie_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))
app = Flask(__name__)

# sample list of options
options = movies['title'].values
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distance = similarity[movie_index]
    movie_list = sorted(list(enumerate(distance)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movie_posters = []
    recommended_movie = []
    for i in movie_list:
        id = movies.iloc[i[0]].id
        recommended_movie_posters.append(fetch_poster(id))
        recommended_movie.append(movies.iloc[i[0]].title)
    return recommended_movie, recommended_movie_posters
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_options', methods=['POST'])
def get_options():
    input_text = request.form['input']
    matching_options = []
    for option in options:
        if input_text.lower() in option.lower():
            matching_options.append(option)
    return jsonify(options=matching_options)

@app.route('/submit_option', methods=['POST'])
def submit_option():
    selected_option = request.form['search-options']
    movierelated,movieposter=recommend(selected_option)
    return render_template('search.html',movieposter=movieposter,movierelated=movierelated,movie=selected_option)

if __name__ == '__main__':

    app.run(debug=True,host='0.0.0.0')