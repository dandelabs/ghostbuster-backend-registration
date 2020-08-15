from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from ..models  import Item
from ..serializers import ItemsSerializer
from rest_framework.decorators import api_view

