# Generated by Django 3.0.4 on 2020-04-01 07:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_auto_20200401_0752'),
        ('films', '0004_auto_20200331_0538'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Suggest',
        ),
    ]