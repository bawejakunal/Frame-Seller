"""
@authors: Siddharth Shah, Kunal Baweja, Akshay Nagpal

Stripe Demo Business Logic
"""

#standard modules
from __future__ import print_function
import os
import json
from datetime import datetime

#django modules
from django.utils.datastructures import MultiValueDictKeyError
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.db import IntegrityError

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
from api.models import Product, Order
from api.serializers import (ProductSerializer, OrderSerializer,
                             OrderDetailSerializer)
import stripe
from async_promises import Promise

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
stripe.api_key = load_key("api/key.json")
#stripe.api_key = os.environ['STRIPE_API_KEY']


def charge_customer(order_id, product_id, stripe_token):
    """
    charge the customer using one time token
    """
    product = Product.objects.get(pk=product_id)
    try:
        charge = stripe.Charge.create(
            amount=int(product.price*100),
            currency="usd",
            metadata={"order_id": order_id},
            source=stripe_token)

        order = Order.objects.get(pk=order_id)
        if charge["paid"] is True:
            order.paymentstatus = Order.PAID
            order.save()
            print("Order " + str(order.id) + " paid")
        elif charge["paid"] is False:
            order.paymentstatus = Order.FAILED
            order.save()
            print("Order " + str(order.id) + " declined")

        return charge

    except stripe.error.InvalidRequestError as error:
        print(error)
    except stripe.error.APIConnectionError as error:
        print(error)
    except stripe.error.AuthenticationError as error:
        print(error)
    except stripe.error.RateLimitError as error:
        print(error)
    except Exception as error:
        print(error)
    return None


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
        orders = Order.objects.filter(user=request.user.id).\
                select_related('product')
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'POST':
        try:
            data = request.data
            data['user'] = request.user.id
            data['orderdate'] = datetime.now()
            data['paymentstatus'] = "UNPAID"
        except KeyError as error:
            print(error)

        serializer = OrderSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            """
            Promise magic is here
            """
            order_id = serializer.data['id']
            _promise = Promise(lambda resolve, reject:
                               reject(Exception('Payment Failed')\
                                if charge_customer(order_id, data['product'],
                                                   data['token']) is None else
                                      resolve('Payment Processed')))

            """
            Process payment in promise and update db
            """
            _promise.then(lambda result: print(result)).\
            catch(lambda error: print(error))

            return Response({'success':True}, status=status.HTTP_202_ACCEPTED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#TODO: restrict spam
@api_view(['POST'])
def signup(request):
    """
    Sign up a new user on stripe_demo
    """
    try:
        data = request.data
        email = data["email"].strip().strip("'").strip('"')
        password = data["password"].strip().strip("'").strip('"')
        first_name = data["first_name"].strip().strip("'").strip('"')
        last_name = data["last_name"].strip().strip("'").strip('"')
        username = email

        if email == "":
            raise ValueError("Email")
        if password == "":
            raise ValueError("Password")
        if first_name == "":
            raise ValueError("First Name")
        if last_name == "":
            raise ValueError("Last Name")

        user = User.objects.create_user(username, email, password)
        user.first_name = first_name
        user.last_name = last_name
        user.save()

        return HttpResponse(json.dumps({"success":True}),
                            content_type="application/json")

    except (KeyError, TypeError, ValueError, MultiValueDictKeyError) as error:
        error = str(error).strip("'").strip('"')
        error += " is a required field"

    except IntegrityError:
        error = "User already exists!"

    return HttpResponse(json.dumps({"success":False, "error": error}),
                        status=status.HTTP_400_BAD_REQUEST,
                        content_type="application/json")
