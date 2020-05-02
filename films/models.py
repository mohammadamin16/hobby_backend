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
