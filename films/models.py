from django.db import models


class Film(models.Model):
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length=100)
    icon = models.URLField()
