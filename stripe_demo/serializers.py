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
