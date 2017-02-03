from django.db import models


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
    STATUS = (
        (0, 'Not Charged'),
        (1, 'Charged'),
        (2, 'Failed'),
    )

    userid = models.CharField(max_length=20)
    productid = models.ForeignKey(Product)
    orderdate = models.DateTimeField()
    token = models.CharField(max_length=30)
    paymentstatus = models.IntegerField(choices=STATUS)
