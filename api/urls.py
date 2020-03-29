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
]
