import jwt
from django.contrib.auth.signals import user_logged_in

from django.views.decorators.csrf import csrf_exempt
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_jwt.settings import api_settings
from rest_framework_jwt.serializers import jwt_payload_handler
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_200_OK
)

from rest_framework.response import Response

from ..auth.backend import ModelAuthentication
from appProjectRESTFul import settings
from ..utils.response import ResponseHttp

@csrf_exempt
@api_view(["POST"])
@permission_classes((AllowAny,))
def login(request):

    username = request.data.get("username")
    password = request.data.get("password")

    if username is None or password is None:
        return Response({'error': 'Please provide both username and password'},
                        status=HTTP_400_BAD_REQUEST)

    user = ModelAuthentication.authenticate(
        request, username=username, password=password)

    if not user:
        return Response({'error': 'User not found'},
                        status=HTTP_404_NOT_FOUND)


    payload = jwt_payload_handler(user)
    token = jwt.encode(payload, settings.SECRET_KEY)
    user_logged_in.send(sender=user.__class__,
                        request=request, user=user)
    
    response = ResponseHttp(token, None)

    return Response(response.data,
                    status=HTTP_200_OK)
