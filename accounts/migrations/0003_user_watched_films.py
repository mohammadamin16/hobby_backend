# Generated by Django 3.0.4 on 2020-03-29 11:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20200329_0938'),
        ('accounts', '0002_user_fav_list'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='watched_films',
            field=models.ManyToManyField(blank=True, related_name='watched', to='films.Film'),
        ),
    ]
