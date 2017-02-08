"""
djangorestframerwork serializer of objects
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from stripe_demo.models import Product, Order


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer user data
    """
    class Meta:
        """
        User metadata
        """
        model = User
        fields = ('id', 'password', 'username', 'email', 'first_name', 'last_name')

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
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(),
                                              many=False)
    product = \
            serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(),
                                               many=False)
    class Meta:
        """
        Order metadata
        """
        model = Order
        fields = ('id', 'user', 'orderdate', 'token', 'paymentstatus',
                  'product')


class OrderDetailSerializer(serializers.ModelSerializer):
    """
    Serialize Order Details
    """
    product = ProductSerializer(read_only=True)
    class Meta:
        """
        Order metadata
        """
        model = Order
        fields = ('id', 'user', 'orderdate', 'paymentstatus', 'product')
