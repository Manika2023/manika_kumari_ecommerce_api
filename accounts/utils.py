# utils.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError

# function for token expired 
def custom_exception_handler(exc, context):
    # calling default DRF handler
    response = exception_handler(exc, context)

    if isinstance(exc, (InvalidToken, TokenError)):
        return Response({
            "message": "Your token is expired or invalid"
        }, status=401)

    # fallback to default response
    print("response is ",response)
    return response
