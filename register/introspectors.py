"""
Custom authentication module
Create your Authentication classes here. Simply extend the base class and override the authenticate method.
Use the Boiler Plate below and replace the app_name to authenticate the token against for that specific app.

Boiler Plate -

class MyCustomGemsOAuth2Authenticator(BaseAuthentication):
    def authenticate(self, request):
        return introspect_request_and_get_user(request, "app_name"), None

"""

from django.conf import settings
from register.gems_oauth2_authenticator import introspect_request_and_get_user
from rest_framework import status
from django.http import JsonResponse
from rest_framework.exceptions import APIException

def gems_oauth_authentication(api_func):
    def wrapper(*args, **kwargs):
        # print args
        # print kwargs
        try:
            introspect_request_and_get_user(args[0], settings.GEMS_OAUTH_INTROSPECTOR['CLIENT_APP_NAME'])

        except APIException as e:
            return JsonResponse({},status=e.status_code)
        except Exception as e:
            return JsonResponse(e.__dict__,
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return api_func(*args, **kwargs)

    return wrapper



