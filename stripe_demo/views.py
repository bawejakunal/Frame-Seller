"""
@authors: Siddharth Shah, Kunal Baweja, Akshay Nagpal

Stripe Demo Business Logic
"""

#standard modules
import os
import json
from datetime import datetime
import requests

#django modules
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from django.http import HttpResponse
from django.views.decorators.http import require_POST
from django.http.response import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

#rest api development framework
from rest_framework import status
from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.authentication import (SessionAuthentication,
                                           BasicAuthentication)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from rest_framework_jwt.authentication import JSONWebTokenAuthentication

#stripe sdk
from stripe_demo.models import Product, Order
from stripe_demo.serializers import ProductSerializer, OrderSerializer
import stripe

@api_view(['GET'])
@authentication_classes((SessionAuthentication, BasicAuthentication, JSONWebTokenAuthentication))
@permission_classes((IsAuthenticated,))
def get_products(request):
    """
    get list of products
    """
    products = Product.objects.all()
    serializer = ProductSerializer(products, many=True)
    return Response(serializer.data)


@csrf_exempt
@require_POST
def signup(request):
    """
    Sign up a new user on stripe_demo
    """
    try:
        username = request.POST["email"]
        password = request.POST["password"]
        first_name = request.POST["firstname"]
        last_name = request.POST["lastname"]
        email = username

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return HttpResponse(json.dumps({"success":True}),
                             content_type="application/json")

    except (KeyError, TypeError, MultiValueDictKeyError) as error:
        error = error

    except IntegrityError:
        error = "User already exists!"

    return HttpResponse(json.dumps({"success":False, "error": error}),
                        status=400, content_type="application/json")


def load_key(keyfile):
    """
    A more secure way to load API keys is to set them in
    os environement variable and read that using os.environ

    Load authentication key from json formatted keyfile

    Expected keyfile content:
    { "stripe_api_key": "YOUR_STRIPE_API_KEY" }
    """
    try:
        if not (os.path.exists(keyfile) or os.path.isfile(keyfile)):
            raise OSError('file does not exist')

        with open(keyfile, 'r') as handle:
            keydata = json.load(handle)
            keydata = keydata['stripe_api_key']
    except:
        keydata = None

    return keydata

#set api key for stripe requests
stripe.api_key = load_key("stripe_demo/key.json")


@api_view(['GET', 'POST'])
@authentication_classes((SessionAuthentication, BasicAuthentication,
                         JSONWebTokenAuthentication))
@permission_classes((IsAuthenticated,))
def order(request):
    """
    Create an order upon receiving request from client
    upon verifying successful payment through stripe

    On success: returns 201 order creation successful
    On failure: 400 Bad Request with error description in detail parameter of
    json response
    """

    #send list of orders corresponding to orders
    if request.method == 'GET':
        orders = Order.objects.filter(user=request.user.id)
        serializer = OrderSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    #TODO: Stripe Payment using token
    if request.method == 'POST':
        try:
            data = request.data
            data['user'] = request.user.id
            data['orderdate'] = datetime.now()
            data['paymentstatus'] = Order.UNPAID
            data['product'] = request.POST["product_id"]
            data['token'] = request.POST["token"]
        except KeyError as error:
            pass

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#TODO: THIS HAS TO BE COMPLETELY CLIENT SIDE
#REMOVE THIS AND USE /api-token-auth/ endpoint to obtain JWT token to be used
#in subsequent API calls
@csrf_exempt
@require_POST
def process_login(request):
    """
    :param request:
    :return:
    """
    username = request.POST["userEmail"]
    password = request.POST["userPassword"]
    r = requests.post('http://localhost:8000/stripe_demo/api-token-auth/',data={'username': username, 'password': password})
    if(r.status_code==200): # OK
        response = r.json()  # this will be in unicode
        token = str(response)
        return HttpResponse(json.dumps({"success": True, "token": token}), status=200, content_type="application/json")
    else:
        return HttpResponse(json.dumps({"success":False, "token": "NULL"}),status=400, content_type="application/json")
