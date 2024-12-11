import requests
from django.shortcuts import render

# Cheia API pentru TMDb
API_KEY = "29d16459f85cc7d752a2e7be585c84bc"
BASE_URL = "https://api.themoviedb.org/3"


def get_movies_by_genre(genre_id):
    """Obține o listă de filme pe baza genului."""
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


def get_popular_movies():
    """Obține o listă de filme populare."""
    url = f"{BASE_URL}/movie/popular"
    params = {"api_key": API_KEY, "language": "en-US", "page": 1}
    response = requests.get(url, params=params).json()
    return response.get("results", [])


def get_movie_genres_by_id(movie_id):
    """Obține genurile unui film pe baza ID-ului."""
    movie_details_url = f"{BASE_URL}/movie/{movie_id}"
    params = {"api_key": API_KEY}
    movie_details = requests.get(movie_details_url, params=params).json()
    return movie_details.get("genres", [])


def find_common_movie(genres_person1, genres_person2):
    """Găsește un film care să aparțină genurilor comune."""
    # Găsește genurile comune
    common_genres = set(genres_person1) & set(genres_person2)
    if not common_genres:
        return []

    # Construiește URL-ul pentru a descoperi filme
    discover_url = f"{BASE_URL}/discover/movie"
    params = {
        "api_key": API_KEY,
        "with_genres": ",".join(str(genre) for genre in common_genres),  # Genurile sunt întregi
        "sort_by": "popularity.desc",
    }
    response = requests.get(discover_url, params=params).json()
    return response.get("results", [])


def movie_match(request):
    """View-ul pentru potrivirea filmelor."""
    popular_movies = get_popular_movies()
    movie1_id = request.GET.get('movie1')
    movie2_id = request.GET.get('movie2')
    recommendation = []

    if movie1_id and movie2_id:
        # Obține genurile filmelor selectate
        genres1 = [genre['id'] for genre in get_movie_genres_by_id(movie1_id)]
        genres2 = [genre['id'] for genre in get_movie_genres_by_id(movie2_id)]
        recommendation = find_common_movie(genres1, genres2)

    return render(request, 'movies/movie_match.html', {
        "popular_movies": popular_movies,
        "movie1_id": movie1_id,
        "movie2_id": movie2_id,
        "recommendation": recommendation,
    })


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