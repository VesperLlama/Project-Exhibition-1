from django.shortcuts import render
import json
import urllib.request
from . import keys
from django.http import JsonResponse

def searchMovie(request):
    if request.method == 'GET':
        search = request.GET.get('term')
        if search:
            # Get movie ID from Search
            id = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key="+keys.api_key+"&language=en-US&query="+search+"&page=1&include_adult=false").read()
            id_data = json.loads(id)
            id = []
            x = 0
            for i in id_data['results']:
                id.append(str(id_data['results'][x]['title']))
                x = x+1

            return JsonResponse(id,safe=False)
        else:
            id = []
            movie = ''

def getMovie(request):
    if request.method == 'POST':
        movie = str(request.POST.get('search'))
        # Get movie ID from Search
        id = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key="+keys.api_key+"&language=en-US&query="+movie+"&page=1&include_adult=false").read()
        id_data = json.loads(id)
        id = ''
        id = str(id_data['results'][0]['id'])
        print(id)

        # Get the recommendations
        res = urllib.request.urlopen("https://api.themoviedb.org/3/movie/"+id+"/recommendations?api_key="+keys.api_key+"&language=en-US&page=1").read()
        json_data = json.loads(res)
        # print(json_data)
    else:
        movie = ''
        json_data = {}
        id = {}

    return render(request, 'index.html', {'json_data': json_data})


def getArtist(request):
    if request.method == 'POST':
        artist = str(request.POST.get('search'))
        res = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="+artist+"&api_key="+keys.lastfm_key+"&format=json").read()
        json_data = json.loads(res)
    else:
        json_data = {}
    
    return render(request, 'songs.html', {'json_data': json_data})

def searchArtist(request):
    if request.method == 'GET':
        artist = str(request.GET.get('term'))
        id = []
        res = urllib.request.urlopen("http://ws.audioscrobbler.com/2.0/?method=artist.search&artist="+artist+"&api_key="+keys.lastfm_key+"&format=json").read()
        json_data = json.loads(res)
        x = 0
        for i in json_data['results']['artistmatches']['artist']:
            id.append(str(json_data['results']['artistmatches']['artist'][x]['name']))
            x = x+1

        return JsonResponse(id,safe=False)
    else:
        id = []

def index(request):
    return render(request, 'index.html')

def songs(request):
    return render(request, 'songs.html')
