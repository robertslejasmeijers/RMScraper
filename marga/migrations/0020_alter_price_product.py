# Generated by Django 4.0.3 on 2022-04-07 13:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('marga', '0019_remove_product_date_time_grab'),
    ]

    operations = [
        migrations.AlterField(
            model_name='price',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='prods', to='marga.product'),
        ),
    ]
