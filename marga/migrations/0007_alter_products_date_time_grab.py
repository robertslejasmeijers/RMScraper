# Generated by Django 4.0.3 on 2022-03-27 20:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0006_alter_products_date_time_grab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='products',
            name='date_time_grab',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
