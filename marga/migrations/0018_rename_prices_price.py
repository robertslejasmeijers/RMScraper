# Generated by Django 4.0.3 on 2022-04-07 12:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0017_remove_product_discount_period_remove_product_price_and_more'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Prices',
            new_name='Price',
        ),
    ]