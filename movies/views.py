import requests
from django.shortcuts import render

# Cheia API pentru TMDb
API_KEY = "29d16459f85cc7d752a2e7be585c84bc"
BASE_URL = "https://api.themoviedb.org/3"


def get_movies_by_genre(genre_id):
    url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": genre_id,
        "sort_by": "popularity.desc",
        "language": "en-US",
    }
    response = requests.get(url, params=params)
    movies = response.json().get("results", [])

    # Adaugă URL-ul complet pentru postere
    for movie in movies:
        if movie.get("poster_path"):
            movie["poster_url"] = f"https://image.tmdb.org/t/p/w500{movie['poster_path']}"

    return movies

def home(request):
    genres = {
        "Action": 28,
        "Comedy": 35,
        "Drama": 18,
        "Horror": 27,
        "Romance": 10749,
    }

    selected_genre = request.GET.get('genre')
    movies = []
    if selected_genre:
        genre_id = genres.get(selected_genre)
        if genre_id:
            movies = get_movies_by_genre(genre_id)

    return render(request, 'movies/home.html', {
        "genres": genres.keys(),
        "movies": movies,
        "selected_genre": selected_genre,
    })