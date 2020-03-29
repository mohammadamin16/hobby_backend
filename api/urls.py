from django.urls import path
from api import views

app_name = 'api'


urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login, name='login'),
    path('signup', views.signup, name='signup'),
    path('search_film', views.search_film, name='search-film'),
    path('fav', views.add_to_fav, name='add-to-fav'),
    path('watch', views.add_to_watch, name='add-to-watch'),
    path('friendship_request', views.friendship_request, name='friendship-request'),
    path('accept_request', views.accept_request, name='accept-request'),
    path('deny_request', views.deny_request, name='deny-request'),
    path('remove_friend', views.remove_friend, name='remove_friend'),
    path('get_requests', views.get_requests, name='get-request'),
    path('suggest', views.suggest, name='suggest'),
]
