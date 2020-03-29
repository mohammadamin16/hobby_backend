# Generated by Django 3.0.4 on 2020-03-29 10:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('films', '0002_auto_20200329_0938'),
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='fav_list',
            field=models.ManyToManyField(blank=True, related_name='fav_list', to='films.Film'),
        ),
    ]
