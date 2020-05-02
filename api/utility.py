from . import db
import json


def user2json(_user):
    try:
        avatar_link = db.get_avatar_link(_user.username)
    except:
        avatar_link = db.get_avatar_default()

    return {'username': _user.username,
            'name': _user.name,
            'bio': _user.bio,
            'avatar': avatar_link
            }


def films2json(films):
    response = []
    for film in films:
        response.append(film2json(film))
    return response


def users2json(_users):
    users = []
    for _user in _users:
        users.append(user2json(_user))
    return users


def film2json(film):
    return {'imdbID': film.imdb_id,
            'title': film.title,
            'poster': film.poster,
            'year': film.year,
            'rating': film.rating,
            'director': film.director,
            'writer': film.writer,
            'countries': film.countries,
            'cast': film.cast,
            'synopsis': film.synopsis,
            'icon': film.icon}


def get_data(request):
    try:
        data = json.loads(request.body.decode('utf-8'))
    except:
        data = request.POST
    return data


def get_files(request):
    try:
        files = json.loads(request.body.decode('utf-8'))
    except:
        files = request.FILES
    return files


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

