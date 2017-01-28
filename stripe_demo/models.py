from django.db import models


class Product(models.Model):
    """
        Model for Products
    """
    price = models.FloatField()
    description = models.CharField(max_length=255)
    url = models.CharField(max_length=200)