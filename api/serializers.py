"""
djangorestframerwork serializer of objects
"""
from rest_framework import serializers
from django.contrib.auth.models import User
from api.models import Product, Order

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer user data
    """
    class Meta:
        """
        User metadata
        """
        model = User
        fields = ('id', 'password', 'username', 'email', 'first_name',
                  'last_name')
        extra_kwargs = {
            'password': {'write_only': True}
        }

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


class PaymentStatusField(serializers.Field):
    """
    Payment status field in Order model
    """
    def __init__(self, *args, **kwargs):
        super(PaymentStatusField, self).__init__(*args, **kwargs)

    def to_representation(self, obj):
        """
        read representation

        obj = numerical representation
        """
        try:
            return Order.STATUS[obj][1]
        except:
            return None

    def to_internal_value(self, data):
        """
        Internal Representation
        """
        for status in Order.STATUS:
            if data == status[1]:
                return status[0]
        
        raise serializers.ValidationError('Invalid Payment Status')

class OrderSerializer(serializers.ModelSerializer):
    """
    Serialize Order of Product
    """
    paymentstatus = PaymentStatusField()
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
    paymentstatus = PaymentStatusField()
    product = ProductSerializer(read_only=True)
    class Meta:
        """
        Order metadata
        """
        model = Order
        fields = ('id', 'user', 'orderdate', 'paymentstatus', 'product')
