from django.shortcuts import render
import json
import urllib.request
from . import keys
from django.http import JsonResponse


def search_movie(request):
    if request.method == 'GET':
        search = request.GET.get('search')
        if search:
            # Get movie ID from Search
            id = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key="+keys.api_key+"&language=en-US&query="+search+"&page=1&include_adult=false").read()
            id_data = json.loads(id)
            id = []
            x = 0
            for i in id_data['results']:
                id.append(str(id_data['results'][x]['title']))
                x = x+1

            return JsonResponse({
                'status': True,
                'id': id
            })
        else:
            id = []
            movie = ''

def getMovie(request):
    if request.method == 'GET':
        movie = str(request.GET.get('movie'))

        # Get movie ID from Search
        id = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key="+keys.api_key+"&language=en-US&query="+movie+"&page=1&include_adult=false").read()
        id_data = json.loads(id)
        id = ''
        id = str(id_data['results'][0]['id'])

        # Get the recommendations
        res = urllib.request.urlopen("https://api.themoviedb.org/3/movie/"+id+"/recommendations?api_key="+keys.api_key+"&language=en-US&page=1").read()
        json_data = json.loads(res)
    else:
        movie = ''
        json_data = {}
        id = {}

    return render(request, 'index.html', {'json_data': json_data})

def index(request):
    return render(request, 'index.html')
