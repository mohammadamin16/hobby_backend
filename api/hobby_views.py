from django.http import JsonResponse
from api.models import Suggestion, Notification, Action
from films.models import Film
from accounts.models import User
from .utility import get_data, notifications2json, films2json
from django.views.decorators.http import require_http_methods

@require_http_methods(["POST"])
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
    user.notifications.add(notification)
    response = {'msg': 'success'}
    return JsonResponse(response)


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
def remove_fav(request):
    data = get_data(request)
    username = data.get('username')
    film_id = data.get('film_id')
    film = Film.objects.get(imdb_id=film_id)
    user = User.objects.get(username=username)
    user.fav_list.remove(film)
    user.save()
    return JsonResponse({'msg': 'success'})


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
def remove_watch(request):
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
    user.watch_films.remove(film)
    user.save()
    return JsonResponse({'msg': 'success'})


@require_http_methods(["POST"])
def get_favs(request):
    data = get_data(request)
    username = data.get('username')
    user = User.objects.get(username=username)
    favs = user.fav_list.all()
    favs = films2json(favs)
    return JsonResponse({'favs': favs})


@require_http_methods(["POST"])
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
