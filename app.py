from flask import Flask, jsonify, request
import os
import requests
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# TMDb API base URL and API key
TMDB_BASE_URL = 'https://api.themoviedb.org/'
TMDB_API_KEY = '53346baeaaddaa31904af42b061115d3'  # Replace with your actual API key

# API key validation middleware
def validate_api_key(api_key):
    return api_key == os.getenv('API_KEY')

@app.route('/movies', methods=['GET'])
def get_movies():
    api_key = request.headers.get('X-API-Key')
    if not api_key or not validate_api_key(api_key):
        return jsonify({"message": "Unauthorized"}), 401

    # Fetch the list of popular movies from TMDb API
    endpoint = f'{TMDB_BASE_URL}/movie/popular'
    params = {'api_key': TMDB_API_KEY}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        movies = []
        for movie in data.get('results', []):
            movie_details = {
                'title': movie.get('title'),
                'release_year': movie.get('release_date', '')[:4],
                'plot': movie.get('overview'),
                'cast': '',  # TMDb API doesn't provide cast information in this endpoint
                'rating': movie.get('vote_average')
            }
            movies.append(movie_details)
        return jsonify(movies)
    else:
        return jsonify({"message": "Failed to retrieve movie list."}), response.status_code

@app.route('/movies/<movie_name>', methods=['GET'])
def get_movie_by_name(movie_name):
    api_key = request.headers.get('X-API-Key')
    if not api_key or not validate_api_key(api_key):
        return jsonify({"message": "Unauthorized"}), 401

    # Fetch movie details by name from TMDb API
    endpoint = f'{TMDB_BASE_URL}/search/movie'
    params = {'api_key': TMDB_API_KEY, 'query': movie_name}
    response = requests.get(endpoint, params=params)

    if response.status_code == 200:
        data = response.json()
        movie = data.get('results', [])[0]  # Assuming the first result is the closest match
        if movie:
            movie_details = {
                'title': movie.get('title'),
                'release_year': movie.get('release_date', '')[:4],
                'plot': movie.get('overview'),
                'cast': '',  # TMDb API doesn't provide cast information in this endpoint
                'rating': movie.get('vote_average')
            }
            return jsonify(movie_details)
        else:
            return jsonify({"message": "Movie not found"}), 404
    else:
        return jsonify({"message": "Failed to retrieve movie details."}), response.status_code

if __name__ == '__main__':
    app.run()
