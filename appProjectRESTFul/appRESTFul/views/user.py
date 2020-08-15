from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny

from ..models  import User
from ..serializers import UsersSerializer


@api_view(["POST"])
@permission_classes((AllowAny,))
def user_init(request):
    
    user_data = JSONParser().parse(request)
    user_serializer = UsersSerializer(data=user_data)

    if user_serializer.is_valid():
        user_serializer.save()
        return JsonResponse(user_serializer.data, status=status.HTTP_201_CREATED)
    return JsonResponse(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

