# Generated by Django 3.0.4 on 2020-03-31 08:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_user_suggests'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='avatar',
            field=models.ImageField(default='', upload_to='avatars/'),
        ),
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default='', max_length=1000),
        ),
    ]
