from rest_framework import HTTP_HEADER_ENCODING, exceptions

from .redis_handler import (
    get_client_instance,
    add_client_instance
)
from django.conf import settings
from django.utils.translation import gettext_lazy as _
import base64
import requests
from django.utils.six import text_type


def get_authorization_header_and_token(request):
    """
    Return request's 'Authorization:' header, as a bytestring.
    Hide some test client ickyness where the header can be unicode.
    """

    auth = request.META.get("HTTP_AUTHORIZATION", b"")
    if isinstance(auth, text_type):
        # Work around django test client oddness
        auth = auth.encode(HTTP_HEADER_ENCODING)
    return auth


def introspect_request_and_get_user(request, app_name):
    """
    Introspect a token using the Gems OAuth2 introspection endpoint.
    """
    user_auth = get_authorization_header_and_token(request).split()

    if not user_auth or user_auth[0].lower() != b"basic":
        raise exceptions.AuthenticationFailed(_("Invalid header!"))
    if len(user_auth) == 1:
        raise exceptions.AuthenticationFailed(_("Invalid basic header. No credentials provided."))
    elif len(user_auth) > 2:
        raise exceptions.AuthenticationFailed(_(
            "Invalid basic header. Credentials string should not contain spaces."
        ))

    cached_authentication = get_client_instance(user_auth[1].decode("utf-8"))

    if cached_authentication:
        user = {
            "username": cached_authentication["username"],
            "client_id": cached_authentication["client_id"],
        }

        return user

    client_id = settings.GEMS_OAUTH_INTROSPECTOR['CLIENT_ID'].encode('utf-8')
    client_secret = settings.GEMS_OAUTH_INTROSPECTOR['CLIENT_SECRET'].encode('utf-8')
    basic_auth = base64.b64encode(client_id + b":" + client_secret)

    headers = {"Authorization": "Basic {}".format(basic_auth.decode("utf-8"))}
    body = {
        "token": user_auth[1].decode("utf-8"),
        "app_name": app_name
    }

    try:
        response = requests.post(
            settings.GEMS_OAUTH_INTROSPECTOR["INTROSPECTION_URL"],
            data=body,
            headers=headers
        )

    except requests.exceptions.RequestException:
        raise exceptions.AuthenticationFailed(_("Authentication Failed!"))

    if response.status_code != 200:
        raise exceptions.AuthenticationFailed(_("Authentication Failed!"))

    response_body = response.json()
    if response_body.get("active") is False:
        raise exceptions.AuthenticationFailed(_("Authentication Failed!"))

    add_client_instance(user_auth[1].decode("utf-8"), response_body)

    user = {
        "username": response_body["username"],
        "client_id": response_body["client_id"],
    }

    return user
