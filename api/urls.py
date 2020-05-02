from django.urls import path
from . import account_views, film_views, hobby_views

app_name = 'api'

urlpatterns = [
    path('login',              account_views.login,              name='login'),
    path('signup',             account_views.signup,             name='signup'),
    path('get_friends',        account_views.get_friends,        name='get-friends'),
    path('accept_request',     account_views.accept_request,     name='accept-request'),
    path('deny_request',       account_views.deny_request,       name='deny-request'),
    path('remove_friend',      account_views.remove_friend,      name='remove_friend'),
    path('get_requests',       account_views.get_requests,       name='get-request'),
    path('search_people',      account_views.search_people,      name='search-people'),
    path('friendship_request', account_views.friendship_request, name='friendship-request'),
    path('get_people',         account_views.get_people,         name='get-people'),
    path('change_avatar',      account_views.change_avatar,      name='change-avatar'),
    
    path('search_film',        film_views.search_film,           name='search-film'),
    
    path('fav',                hobby_views.add_to_fav,           name='add-to-fav'),
    path('disfav',             hobby_views.remove_fav,           name='remove-from-fav'),
    path('watch',              hobby_views.add_to_watch,         name='add-to-watch'),
    path('unwatch',            hobby_views.remove_watch,         name='unwatch'),
    path('get_notifications',  hobby_views.get_notifications,    name='get-suggests'),
    path('suggest',            hobby_views.create_suggest,       name='suggest'),
    path('get_favs',           hobby_views.get_favs,             name='get-favs'),
]
