from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.views.decorators.http import require_http_methods
from django.db import IntegrityError
from .utility import user2json, users2json, get_data, get_files, films2json, notifications2json
from accounts.models import User
from films.models import Film
from . import db

@require_http_methods(["POST"])
def login(request):
    data = get_data(request)
    username = data.get('username')
    password = data.get('password')

    user = authenticate(username=username, password=password)
    if user is not None:
        msg = 'success'
        response = {'msg': msg, 'user': user2json(user)}
        return JsonResponse(response)

    else:
        msg = "Wrong Username or Password!"
        response = {'msg': msg}
        return JsonResponse(response)


@require_http_methods(["POST"])
def signup(request):
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
        print('EEEEEEEERRRRRRRRRROOOOOOOOOOOOOORRRRRRRRRRRRRR:', e)
        msg = 'this username is taken'
        response = {'msg': msg}
    

    # else:
    #     msg = 'Something went wrong!'
    #     response = {'msg': msg}
  
    return JsonResponse(response)


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
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
    for user in user.requested_users.all():
        requests.append(user2json(user))

    return JsonResponse({'requests': requests})


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
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
    friend.requested_users.remove(friend)
    user.save()
    friend.save()
    return JsonResponse({'msg': 'You denied him/her!'})


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
def get_friends(request):
    data = get_data(request)
    username = data.get('username')
    user = User.objects.get(username=username)
    response = {
        'friends': users2json(user.friends.all())
    }
    return JsonResponse(response)


@require_http_methods(["POST"])
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


@require_http_methods(["POST"])
def get_people(request):
    users = User.objects.all()
    response = {'users': users2json(users)}
    return JsonResponse(response)


@require_http_methods(["POST"])
def change_avatar(request):
    data = get_data(request)
    files = get_files(request)
    username = data.get('username')
    file = request.FILES['image']
    user = User.objects.get(username=username)
    user.avatar.save("{}/{}.png".format(username, username), file)
    db.handle_uploaded_file(file, username)

    db.upload_avatar(user.avatar.path, username)

    return JsonResponse({'msg': 'success'})
