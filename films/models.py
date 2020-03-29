from django.db import models


class Film(models.Model):
    imdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    icon = models.URLField()

    def __str__(self):
        return self.title


class Suggest(models.Model):
    title = models.CharField(max_length=300)
    suggester = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='suggester')
    film = models.ForeignKey('films.Film', on_delete=models.CASCADE, related_name='suggested_film')

    def __str__(self):
        return self.title
