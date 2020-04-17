from django.db import models


class Film(models.Model):
    imdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    icon = models.URLField()

    poster = models.URLField(blank=True)

    year = models.IntegerField(blank=True)
    countries = models.CharField(max_length=100,blank=True)
    box_office = models.CharField(max_length=100, default=0,blank=True)

    rating = models.FloatField(blank=True)
    votes = models.IntegerField(blank=True)

    cast = models.CharField(max_length=200,blank=True)
    writer = models.CharField(max_length=200,blank=True)
    director = models.CharField(max_length=200,blank=True)

    synopsis = models.TextField(blank=True)

    def __str__(self):
        return self.title


# class Suggest(models.Model):
#     title = models.CharField(max_length=300)
#     suggester = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='suggester')
#     film = models.ForeignKey('films.Film', on_delete=models.CASCADE, related_name='suggested_film')
#
#
#
#     def __str__(self):
#         return self.title
