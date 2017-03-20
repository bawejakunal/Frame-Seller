"""
Payment processing
"""
import os
from lib import stripe

stripe.api_key = os.environ['STRIPE_API_KEY']

def create_charge(order_data):
    try:
        charge = stripe.Charge.create(
            amount=int(order_data['price']*100),
            currency=order_data['currecy'],
            metadata=order_data['metadata'],
            source=order_data['stripe_token'])

        if charge['paid'] is True:
            #set order status as paid
            pass
        else:
            #set order status as failed payment
            pass

        #update order status here

    except stripe.error.InvalidRequestError as error:
        print(error)
        charge = None
    except stripe.error.APIConnectionError as error:
        print(error)
        charge = None
    except stripe.error.AuthenticationError as error:
        print(error)
        charge = None
    except stripe.error.RateLimitError as error:
        print(error)
        charge = None
    finally:
        return charge
