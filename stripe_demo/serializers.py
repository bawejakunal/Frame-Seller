"""
djangorestframerwork serializer of objects
"""
from rest_framework import serializers
from stripe_demo.models import Product, Order

class ProductSerializer(serializers.ModelSerializer):
    """
    Serialize Product list
    """
    class Meta:
        """
        Metadata for Product Serializationt to expose API
        """
        model = Product
        fields = ('id', 'price', 'description', 'url')

class OrderSerializer(serializers.ModelSerializer):
    """
    Serialize Order of Product
    """
    class Meta:
        """
        Order metadata
        """
        model = Order
        fields = ('id', 'user', 'orderdate', 'token', 'paymentstatus',
                  'product')


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serialize Order of Product
    """
    product = ProductSerializer(read_only=True)
    class Meta:
        """
        Order metadata
        """
        model = Order
        fields = ('id', 'user', 'orderdate', 'paymentstatus', 'product')
