# Generated by Django 4.0.3 on 2022-03-30 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0008_urls_barbora_urls_rimi'),
    ]

    operations = [
        migrations.CreateModel(
            name='urls',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('store_id', models.IntegerField(null=True)),
                ('url', models.URLField(null=True)),
            ],
        ),
        migrations.DeleteModel(
            name='urls_barbora',
        ),
        migrations.DeleteModel(
            name='urls_rimi',
        ),
    ]
