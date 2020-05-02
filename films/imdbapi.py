from django.db import IntegrityError
from imdb import IMDb
from films.models import Film
from api.utility import *
from accounts.models import User

def get_film_info(imdb_id:int, l:list, _user: User):
    try:
        film_db = Film.objects.get(imdb_id=imdb_id)
        film = film2json(film_db)
        if _user.fav_list.filter(imdb_id=imdb_id).exists():
            film['like_status'] = True
        else:
            film['like_status'] = False
        
        if _user.watch_films.filter(imdb_id=imdb_id).exists():
            film['watch_status'] = True
        else:
            film['watch_status'] = False

    except:
        film_imdb = get_info(imdb_id)
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
        film_db = Film.objects.create(**film)
        film = film2json(film_db)
        film['like_status'] = False
        film['watch_status'] = False

    l.append(film)



def search(query, results=2, sort_by='rating'):
    imdb = IMDb()
    response = imdb.search_movie_advanced(query, sort=sort_by, results=results)
    results = []
    for movie in response:
        m = movie.getID()
        results.append(m)

    return results


def get_info(movie_id: str):
    ia = IMDb()
    movie = ia.get_movie(movie_id)
    title = movie.get("title")
    year = movie.get("year")
    try:
        cast_people = movie.get('cast')[0:5]
    except (TypeError, KeyError):
        cast_people = ""
    cast_names = []
    for c in cast_people:
        cast_names.append(c.get('name'))
    cast = ", ".join(cast_names)
    countries = ", ".join(movie.get('countries'))
    try:
        box_office = movie.get("box office")['Budget']
    except (TypeError, KeyError, IntegrityError):
        box_office = 0
    try:
        rating = movie.get('rating')
    except (TypeError, KeyError, IntegrityError):
        rating = 0
    try:
        votes = movie.get('votes')
    except (TypeError, KeyError, IntegrityError):
        votes = 0
    cover_url = movie.get("cover url")
    fullsize_poster = movie.get_fullsizeURL()
    writer_people = movie.get('writer')
    write_names = []
    try:
        for w in writer_people:
            write_names.append(w.get('name'))
        writer = ", ".join(write_names)
    except TypeError:
        writer = ""

    director_people = movie.get('director')
    director_names = []
    try:
        for d in director_people:
            director_names.append(d.get('name'))
        director = ", ".join(director_names)
    except TypeError:
        director = ""

    top_250_films = 0 if str(movie.get('top 250 films')) == 'None' else movie.get('top 250 films')
    try:
        synopsis = movie.get('synopsis')[0][:500] + "..."
    except TypeError:
        synopsis = ""
    info = dict(
        title=title,
        imdbId=movie_id,
        year=year,
        cast=cast,
        countries=countries,
        box_office=box_office,
        rating=rating,
        votes=votes,
        cover_url=cover_url,
        fullsize_poster= fullsize_poster,
        writer=writer,
        director=director,
        top_250_films=top_250_films,
        synopsis=synopsis
    )
    return info
