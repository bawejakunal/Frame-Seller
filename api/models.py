"""
stripe_demo models for Buy Amazing Photos
"""
from django.db import models
from django.contrib.auth.models import User

class Product(models.Model):
    """
    Model for Products
    """
    price = models.FloatField()
    description = models.TextField()
    url = models.CharField(max_length=200)

    def __str__(self):
        return self.description

class Order(models.Model):
    """
    Model for Orders
    """
    UNPAID = 0
    PAID = 1
    FAILED = 2

    STATUS = (
        (UNPAID, 'UNPAID'),
        (PAID, 'PAID'),
        (FAILED, 'FAILED'),
    )

    user = models.ForeignKey(User)
    product = models.ForeignKey(Product)
    orderdate = models.DateTimeField()
    token = models.CharField(max_length=30)
    paymentstatus = models.IntegerField(choices=STATUS)
