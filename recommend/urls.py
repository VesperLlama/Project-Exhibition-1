from django.urls import path
from . import views
from recommend.views import *
# from .views import searchMovie

urlpatterns = [
    path('', views.index, name='index'),
    path('search_movie/', views.searchMovie, name='search_movie'),
    path('movie/', views.getMovie, name='movie'),
    path('search_artist/', views.searchArtist, name='search_artist'),
    path('artist/', views.getArtist, name='artist'),
    path('songs/', views.getSongs, name='songs'),
    path('search_songs/', views.searchSongs, name='search_songs'),

]