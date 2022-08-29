from django.shortcuts import render
import json
import urllib.request
from . import keys

def index(request):
    if request.method == 'POST':
        movie = request.POST['movie']

        # Get movie ID from Search
        id = urllib.request.urlopen("https://api.themoviedb.org/3/search/movie?api_key="+keys.api_key+"&language=en-US&query="+movie+"&page=1&include_adult=false").read()
        id_data = json.loads(id)
        id = str(id_data['results'][0]['id'])

        # Get the recommendations
        res = urllib.request.urlopen('https://api.themoviedb.org/3/movie/'+id+'/recommendations?api_key='+keys.api_key+'&language=en-US&page=1').read()
        json_data = json.loads(res)
    else:
        movie = ''
        json_data = {}

    return render(request, 'index.html', {'json_data':json_data})
