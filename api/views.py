import json
import threading

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from accounts.models import User
from films.models import Film

from films import imdbapi


def get_data(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = request.POST
    return data


def index(request):
    return HttpResponse("Hello What's Up?")


def json_user(user):
    username = user.username
    name     = user.name
    return {'username': username, 'name': name}


def login(request):
    if request.method == 'POST':
        data = get_data(request)
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            msg = 'welcome'
            response = {'msg': msg,
                        'user': json_user(user)}

            return JsonResponse(response)

        else:
            msg = "Wrong Username or Password!"
            response = {'msg': msg}
            return JsonResponse(response)



    else:
        return HttpResponse("What's Up?")


def signup(request):
    data = get_data(request)
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    try:
        user = User.objects.create(username=username,name=name)
        user.set_password(password)
        user.save()
        msg = 'welcome'
        response = {'msg': msg,
                    'user': json_user(user)}

    except Exception as e:
        msg = e.args
        response = {'msg': msg}
        print(msg)

    return JsonResponse(response)


def search_film(request):
    data = get_data(request)
    query = data.get('query')
    ids = imdbapi.search(query, results=4)
    films = []
    threads = []

    def get_info(imdb_id, l: list):
        film_imdb = imdbapi.get_info(imdb_id)
        film = dict(
            imdb_id=film_imdb['imdbId'],
            title=film_imdb['title'],
            icon=film_imdb['cover_url'],)
        try:
            film_db = Film.objects.get(imdb_id=film_imdb['imdbId'])
        except:
            film_db = Film.objects.create(**film)

        l.append(film)

    for ID in ids:
        t1 = threading.Thread(target=get_info, args=(ID, films))
        t1.start()
        threads.append(t1)

    for t in threads:
        t.join()

    response = {'films': films}

    return JsonResponse(response)


def add_to_fav(request):
    data = get_data(request)
    username = data.get('username')
    film_id = data.get('film_id')
    film = Film.objects.get(imdb_id=film_id)
    user = User.objects.get(username=username)
    user.fav_list.add(film)
    user.save()
    return JsonResponse({'msg': 'success'})


def add_to_watch(request):
    data = get_data(request)
    username = data.get('username')
    film_id = data.get('film_id')
    film = Film.objects.get(imdb_id=film_id)
    user = User.objects.get(username=username)
    user.watch_films.add(film)
    user.save()
    return JsonResponse({'msg': 'success'})



