"""
Stripe demo utility method
"""
from datetime import datetime
from rest_framework_jwt.settings import api_settings

def jwt_payload_handler(user):
    """
    override rest_framework_jwt.utils.jwt_payload_handler
    """
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'username': user.username,
        'email': user.email,
        'exp': datetime.utcnow() + api_settings.JWT_EXPIRATION_DELTA
    }
