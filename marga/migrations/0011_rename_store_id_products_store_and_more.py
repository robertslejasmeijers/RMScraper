# Generated by Django 4.0.3 on 2022-03-31 12:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0010_stores_alter_products_store_id_alter_urls_store_id'),
    ]

    operations = [
        migrations.RenameField(
            model_name='products',
            old_name='store_id',
            new_name='store',
        ),
        migrations.RenameField(
            model_name='urls',
            old_name='store_id',
            new_name='store',
        ),
    ]
