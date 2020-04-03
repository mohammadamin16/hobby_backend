import json
import threading

from django.contrib.auth import authenticate
from django.http import HttpResponse, JsonResponse
from accounts.models import User
from api.models import Suggestion, Notification
from films.models import Film

from itertools import chain
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
            msg = 'success'
            response = {'msg': msg,
                        'user': user2json(user)}

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
        msg = 'success'
        response = {'msg': msg,
                    'user': user2json(user)}

    except Exception as e:
        msg = e.args
        response = {'msg': msg}
        print(msg)

    return JsonResponse(response)


def search_film(request):
    """
    search in imdb database and save searched films to our own db
    :param request: (query, username)
    :return: films
    """
    data = get_data(request)
    query = data.get('query')
    username = data.get('username')
    user = User.objects.get(username=username)

    ids = imdbapi.search(query, results=4)
    films = []
    threads = []

    def get_info(imdb_id, l, _user: User):
        film_imdb = imdbapi.get_info(imdb_id)
        film = dict(
            imdb_id=film_imdb['imdbId'],
            title=film_imdb['title'],
            icon=film_imdb['cover_url'],
            poster=film_imdb['fullsize_poster'],
            year=film_imdb['year'],
            countries=film_imdb['countries'],
            box_office=film_imdb['box_office'],
            rating=film_imdb['rating'],
            votes=film_imdb['votes'],
            cast=film_imdb['cast'],
            writer=film_imdb['writer'],
            director=film_imdb['director'],
            synopsis=film_imdb['synopsis'],
        )
        try:
            film_db = Film.objects.get(imdb_id=film_imdb['imdbId'])
            if _user.fav_list.filter(imdb_id=imdb_id).exists():
                film['like_status'] = True
            else:
                film['like_status'] = False
        except:
            film_db = Film.objects.create(**film)
            film['like_status'] = False

        l.append(film)

    for ID in ids:
        t1 = threading.Thread(target=get_info, args=(ID, films, user))
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
    print('film_id', film_id)
    film = Film.objects.get(imdb_id=film_id)
    user = User.objects.get(username=username)
    print('LIKING FILM {} user: {}'.format(user, film))
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


def film2json(film):
    return {'imdbID':film.imdb_id,
            'title':film.title,
            'poster':film.poster,
            'icon':film.icon}


def user2json(_user):
    return {'username': _user.username,
            'name': _user.name,
            'bio': _user.bio,
            'avatar': 'http://192.168.1.249:8000' + _user.avatar.url}


def users2json(_users):
    users = []
    for _user in _users:
        users.append(user2json(_user))
    return users


def search_people(request):
    data = get_data(request)
    query = data.get('query')
    username = data.get('username')
    user = User.objects.get(username=username)
    r1 = User.objects.filter(username__contains=query)
    r2 = User.objects.filter(name__contains=query)
    result_list = r1 | r2
    users = []
    # if u isn't in user's requested:relation = normal
    # if u is in user's requested:relation = requested
    # if u is in user's friends:relation = friend
    for user in result_list:
        users.append(user)
    response = {'users': users2json(users)}
    return JsonResponse(response)


def create_suggest(request):
    data = get_data(request)
    username = data.get('username')
    film_id = data.get('film_id')
    title = data.get('title')
    text = data.get('text')

    user = User.objects.get(username=username)
    film = Film.objects.get(imdb_id=film_id)
    suggest = Suggestion.objects.create(
        title=title,
        text=text,
        film=film,
    )
    suggest.save()
    notification = Notification.objects.create(
        owner=user,
        kind='suggest',
        suggest=suggest
    )
    notification.save()
    friends = user.friends.all()
    for friend in friends:
        friend.notifications.add(notification)
        friend.save()

    response = {'msg': 'success'}
    return JsonResponse(response)


def suggest2json(_suggest):
    return {'title': _suggest.title,
            'text': _suggest.text,
            'film': film2json(_suggest.film)}


def notification2json(_notification):
    return {'owner': user2json(_notification.owner),
            'kind': _notification.kind,
            'suggest': suggest2json(_notification.suggest),
            'action': _notification.action,}


def notifications2json(_notifications):
    l = []
    for noti in _notifications:
        l.append(notification2json(noti))
    return l


def get_notifications(request):
    data = get_data(request)
    try:
        username = data.get('username')
        user = User.objects.get(username=username)
        notifications = user.notifications.all()
        response = {
            'msg':'success',
            'notifications':notifications2json(notifications)
        }
    except Exception as e:
        response = {
            'msg': e,
        }

    return JsonResponse(response)
