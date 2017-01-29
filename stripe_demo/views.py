"""
    Stripe Demo Webservice Business Logic
"""

import json

from stripe_demo.models import Product
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.views.decorators.http import require_GET

@require_GET
def get_products(request):
    """
        function to get all products and send them as json
    :param request:
    :return:
    """
    products = Product.objects.values()
    product_list = [p for p in products]  # converts ValuesQuerySet into Python list
    return JsonResponse(product_list,safe=False)

