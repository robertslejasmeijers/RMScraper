# Generated by Django 4.0.3 on 2022-03-27 14:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0003_products_discount_period_products_link_to_picture_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='products',
            name='date_time_grab',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
