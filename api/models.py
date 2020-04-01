from django.db import models


class Notification(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('accounts.User', on_delete=models.CASCADE, related_name='notification_owner')
    kind = models.CharField(max_length=100)  # choices: 'suggest' or 'action'
    suggest = models.ForeignKey('Suggestion', on_delete=models.CASCADE, blank=True, null=True)
    action = models.ForeignKey('Action', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.kind + ", " + self.owner.username


class Suggestion(models.Model):
    title = models.CharField(max_length=1000)
    text = models.TextField()
    film = models.ForeignKey('films.Film', on_delete=models.CASCADE, related_name='suggested_film')

    def __str__(self):
        return self.film.title + ", " + self.title


class Action(models.Model):
    event = models.CharField(max_length=100)
    film = models.ForeignKey('films.Film', on_delete=models.CASCADE, related_name='action')

    def __str__(self):
        return self.event + " : " + self.film.title
