from django.db import models
class Products(models.Model):
    name = models.CharField(max_length=255, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_old = models.DecimalField(max_digits=6, decimal_places=2, null=True)
    price_per_unit = models.CharField(max_length=50, null=True)
    link_to_picture = models.CharField(max_length=255, null=True)
    date_time_grab = models.DateTimeField(auto_now_add=True, null=True)
    store_id = models.IntegerField(null=True)
    discount_period = models.CharField(max_length=50, null=True)

class Urls(models.Model):
    store_id = models.IntegerField(null=True)
    url = models.URLField(max_length=200, null=True)