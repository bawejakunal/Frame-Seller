"""
@authors: Siddharth Shah, Kunal Baweja

Stripe Demo Business Logic
"""

import os
import json
from django.contrib.auth.models import User
from django.utils.datastructures import MultiValueDictKeyError
from django.db import IntegrityError
from django.shortcuts import redirect
from django.http.response import HttpResponseRedirect
from stripe_demo.models import Product
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
import stripe

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

@csrf_exempt
@require_POST
def post_order(request):
    """

    :param request:
    :return:
    """

    # TODO: Check for JWT from request
    print(request.POST)
    token = request.POST["stripeToken"]
    productid = request.POST["productid"]
    product = Product.objects.get(id=productid)

    print(stripe.api_key)

    # Charge the user's card:
    charge = stripe.Charge.create(
        amount=product.price,
        currency="usd",
        description=product.description,
        source=token,
    )
    print(charge)

    return redirect("http://stripe6998.s3-website-us-west-2.amazonaws.com/catalog.html")


@require_GET
def get_products(request):
    """
    function to get all products and send them as json
    @param request:
    :return:
    """

    #TODO: Check for JWT from request

    products = Product.objects.values()
    product_list = [p for p in products]  # ValuesQuerySet to Python list
    return JsonResponse(product_list, safe=False)
