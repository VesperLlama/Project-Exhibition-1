from django.shortcuts import render
import json
import urllib.request
import urllib.parse
from . import keys
from django.http import JsonResponse


def searchMovie(request):
    if request.method == "GET":
        search = str(urllib.parse.quote(request.GET.get("term")))
        if search:
            # Get movie ID from Search
            id = urllib.request.urlopen(
                "https://api.themoviedb.org/3/search/movie?api_key="
                + keys.api_key
                + "&language=en-US&query="
                + search
                + "&page=1&include_adult=false"
            ).read()
            id_data = json.loads(id)
            id = []
            x = 0
            for i in id_data["results"]:
                id.append(str(id_data["results"][x]["title"]))
                x = x + 1

            return JsonResponse(id, safe=False)
        else:
            id = []
            movie = ""


def getMovie(request):
    if request.method == "POST":
        movie = str(urllib.parse.quote(request.POST.get("search")))
        # Get movie ID from Search
        id = urllib.request.urlopen(
            "https://api.themoviedb.org/3/search/movie?api_key="
            + keys.api_key
            + "&language=en-US&query="
            + movie
            + "&page=1&include_adult=false"
        ).read()
        id_data = json.loads(id)
        id = ""
        id = str(id_data["results"][0]["id"])
        print(id)

        # Get the recommendations
        res = urllib.request.urlopen(
            "https://api.themoviedb.org/3/movie/"
            + id
            + "/recommendations?api_key="
            + keys.api_key
            + "&language=en-US&page=1"
        ).read()
        json_data = json.loads(res)
    else:
        movie = ""
        json_data = {}
        id = {}

    return render(request, "index.html", {"json_data": json_data})


def getArtist(request):
    if request.method == "POST":
        artist = str(urllib.parse.quote(request.POST.get("search")))
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=artist.getsimilar&artist="
            + artist
            + "&limit=15&api_key="
            + keys.lastfm_key
            + "&format=json"
        ).read()
        json_data = json.loads(res)
        for x in range(15):
            mbid = [json_data["similarartists"]["artist"][x]["mbid"]]
        x = 0
        for i in mbid:
            img = urllib.request.urlopen(
                "https://musicbrainz.org/ws/2/artist/"
                + mbid[x]
                + "?inc=url-rels&fmt=json"
            ).read()
            if img["relations"]["type"] == image:
                img_src.append(img["url"]["resource"])
            if img_src[x].startswith("https://commons.wikimedia.org/wiki/File:"):
                filename = image_url.substring(image_url.lastIndexOf("/") + 1)
                img_src[x] = (
                    "https://commons.wikimedia.org/wiki/Special:Redirect/file/"
                    + filename
                )
    else:
        json_data = {}

    return render(request, "artists.html", {"json_data": json_data, "img_src": img_src})


def searchArtist(request):
    if request.method == "GET":
        artist = str(urllib.parse.quote(request.GET.get("term")))
        id = []
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=artist.search&artist="
            + artist
            + "&api_key="
            + keys.lastfm_key
            + "&format=json"
        ).read()
        json_data = json.loads(res)
        x = 0
        for i in json_data["results"]["artistmatches"]["artist"]:
            id.append(str(json_data["results"]["artistmatches"]["artist"][x]["name"]))
            x = x + 1

        return JsonResponse(id, safe=False)
    else:
        id = []


def searchSongs(request):
    if request.method == "GET":
        track = str((urllib.parse.quote(request.GET.get("term"))))
        id = []
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=track.search&track="
            + track
            + "&api_key="
            + keys.lastfm_key
            + "&format=json"
        ).read()
        json_data = json.loads(res)
        x = 0
        for i in json_data["results"]["trackmatches"]["track"]:
            id.append(
                str(
                    json_data["results"]["trackmatches"]["track"][x]["name"]
                    + " - "
                    + json_data["results"]["trackmatches"]["track"][x]["artist"]
                )
            )
            x = x + 1

        return JsonResponse(id, safe=False)
    else:
        id = []


def getSongs(request):
    if request.method == "POST":
        search = str(request.POST.get("search")).split(" - ")
        track = str(urllib.parse.quote(search[0]))
        artist = str((urllib.parse.quote(search[1])))
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=track.getsimilar&artist="
            + artist
            + "&track="
            + track
            + "&limit=15&api_key="
            + keys.lastfm_key
            + "&format=json"
        ).read()
        json_data_s = json.loads(res)
        covers = getCovers(json_data_s)
        x = 0
        for i in covers:
            json_data_s["similartracks"]["track"][x]["image"] = covers[x]
            x += 1
    else:
        json_data_s = {}

    return render(request, "index.html", {"json_data_s": json_data_s})


def getCovers(info):
    covers = []
    for i in info["similartracks"]["track"]:
        track = str(urllib.parse.quote(i["name"]))
        artist = str(urllib.parse.quote(i["artist"]["name"]))
        res = urllib.request.urlopen(
            "https://ws.audioscrobbler.com/2.0/?method=track.getInfo&api_key="
            + keys.lastfm_key
            + "&artist="
            + artist
            + "&track="
            + track
            + "&format=json"
        ).read()
        json_data = json.loads(res)
        covers.append(json_data["track"]["album"]["image"][3]["#text"])

    return covers


def index(request):
    return render(request, "index.html")
