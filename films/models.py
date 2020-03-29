from django.db import models


class Film(models.Model):
    imdb_id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    icon = models.URLField()

    def __str__(self):
        return self.title