# Generated by Django 4.0.3 on 2022-04-05 15:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0013_url_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='url',
            name='user',
        ),
    ]