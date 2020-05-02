from accounts.models import User
from films.models import Film
from films import imdbapi
import threading
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from .utility import *
from films import imdbapi

@require_http_methods(["POST"])
def search_film(request):
    data = get_data(request)
    query = data.get('query')
    username = data.get('username')
    user = User.objects.get(username=username)

    ids = imdbapi.search(query, results=5)
    films = []
    threads = []

    for ID in ids:
        t1 = threading.Thread(target=imdbapi.get_film_info, args=(ID, films, user))
        t1.start()
        threads.append(t1)

    for t in threads:
        t.join()

    response = {'films': films}

    return JsonResponse(response)
