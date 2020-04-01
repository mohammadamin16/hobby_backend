from django.contrib import admin

from .models import Suggestion, Notification, Action

admin.site.register(Action)
admin.site.register(Notification)
admin.site.register(Suggestion)

