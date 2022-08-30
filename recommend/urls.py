from django.urls import path
from . import views
from recommend.views import *

urlpatterns = [
    path('', views.index, name='index'),
    path('search_movie/', views.search_movie),
    path('movie/', views.getMovie)
]