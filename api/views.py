import json
import threading

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from accounts.models import User
from films.models import Film, Suggest

from films import imdbapi


def get_data(request):
    """
    It tries to catch sent data with post request
    """
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
    """
    :param request: (username, password)
    :return: msg and user (if success)
    """
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
    """
    :param request: (username, password, name)
    :return: msg and user (if success)
    """
    data = get_data(request)
    username = data.get('username')
    password = data.get('password')
    name = data.get('name')
    try:
        user = User.objects.create(username=username, name=name)
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
    """
    search in imdb database and save searched films to our own db
    :param request: (query)
    :return: films
    """
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
    """
    Add a Film to user's Favorite Movies
    :param request: (username, film_id)
    :return: msg
    """
    data = get_data(request)
    username = data.get('username')
    film_id = data.get('film_id')
    film = Film.objects.get(imdb_id=film_id)
    user = User.objects.get(username=username)
    user.fav_list.add(film)
    user.save()
    return JsonResponse({'msg': 'success'})


def add_to_watch(request):
    """
    Add a Film to user's Watch List
    :param request: (username, film_id)
    :return: msg
    """
    data = get_data(request)
    username = data.get('username')
    film_id = data.get('film_id')
    film = Film.objects.get(imdb_id=film_id)
    user = User.objects.get(username=username)
    user.watch_films.add(film)
    user.save()
    return JsonResponse({'msg': 'success'})


def friendship_request(request):
    """
    Add a request to the one user wants to be friend with
    :param request: (username, friend's username)
    :return: msg
    """
    data = get_data(request)
    username = data.get('username')
    friend_username = data.get('friend_username')
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friend_username)
    friend.requested_users.add(user)
    friend.save()
    return JsonResponse({'msg': 'Request Sends!'})


def get_requests(request):
    """
    Returns all the requests for a user
    :param request: (username)
    :return: requests
    """
    data = get_data(request)
    username = data.get('username')
    user = User.objects.get(username=username)
    requests = []
    for r in user.requested_users.all():
        requests.append(r.username)

    return JsonResponse({'msg': 'here they are!', 'requests': requests})


def accept_request(request):
    """
    When user accepts other user's friendship_requests
    :param request: (username, friend_username)
    :return: msg
    """
    data = get_data(request)
    friend_username = data.get('friend_username')
    username = data.get('username')
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friend_username)
    user.friends.add(friend)
    user.requested_users.remove(friend)
    friend.friends.add(user)
    friend.save()
    user.save()
    return JsonResponse({'msg': 'Now you are friends!'})


def deny_request(request):
    """
    When user denies other user's friendship_requests
    :param request: (username, friend_username)
    :return: msg
    """

    data = get_data(request)
    friend_username = data.get('friend_username')
    username = data.get('username')
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friend_username)
    user.requested_users.remove(friend)
    user.save()
    return JsonResponse({'msg': 'You denied him/her!'})


def remove_friend(request):
    """
    When a user ends being friend with another user
    :param request: (username, friend_username)
    :return: msg
    """

    data = get_data(request)
    friend_username = data.get('friend_username')
    username = data.get('username')
    user = User.objects.get(username=username)
    friend = User.objects.get(username=friend_username)
    user.friends.remove(friend)
    friend.friends.remove(user)
    user.save()
    friend.save()
    return JsonResponse({'msg': 'You are not friend with {} anymore(in hobbies!)'.format(friend_username)})


def suggest(request):
    """
    suggest to friends a flim
    :param request: (username, film_id, title of the suggestion)
    :return: msg
    """

    data     = get_data(request)
    film_id  = data.get('film_id')
    title    = data.get('title')
    username = data.get('username')
    user = User.objects.get(username=username)
    film = Film.objects.get(imdb_id=film_id)
    friends = user.friends.all()
    s = Suggest.objects.create(
        title=title,
        film=film,
        suggester=user
    )
    s.save()
    for friend in friends:
        friend.suggests.add(s)
        friend.save()
    return JsonResponse({'msg': 'You just suggest this film to all your friends!'})


def film2json(film):
    return {'imdbID':film.imdb_id,
            'title':film.title,
            'icon':film.icon}


def suggest2json(_suggest):
    return {'title': _suggest.title,
            'film': film2json(_suggest.film),
            'suggester': user2json(_suggest.suggester)}


def user2json(_user):
    return {'username': _user.username,
            'name': _user.name}


def get_suggests(request):
    """
    Returns all the suggestions for a user
    :param request: (username)
    :return: msg
    """

    data = get_data(request)
    username = data.get('username')
    user = User.objects.get(username=username)
    user_suggests = user.get_suggestions()
    suggests = []
    for s in user_suggests:
        suggests.append(suggest2json(s))
    print(suggests)
    return JsonResponse({'msg': 'There are your suggests!',
                         'suggests': suggests
                         })
