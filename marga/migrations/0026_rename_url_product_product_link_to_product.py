# Generated by Django 4.0.3 on 2022-04-20 00:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0025_remove_product_url_product_url_product'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='url_product',
            new_name='link_to_product',
        ),
    ]