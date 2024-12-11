from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('movie-match/', views.movie_match, name='movie_match'),
]