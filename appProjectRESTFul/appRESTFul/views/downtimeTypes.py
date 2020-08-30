from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q

from ..models  import DowntimeType
from ..serializers import DowntimeTypeSerializer
from ..utils.response import ResponseHttp

from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_202_ACCEPTED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_500_INTERNAL_SERVER_ERROR
)

# GET, POST AND DELETE many items
@api_view(['GET', 'POST'])
def downtimeType_list(request):

    try:

        if request.method == 'GET':
            items = list(DowntimeType.objects.all())
            items_serializer = DowntimeTypeSerializer(items, many=True)
            
            return JsonResponse({'result': items_serializer.data, 'error' : ''}, safe=False, status=HTTP_200_OK)
        
        elif request.method == 'POST':
            item_data = JSONParser().parse(request)
            item_serializer = DowntimeTypeSerializer(data=item_data)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error' : ''}, status=HTTP_201_CREATED)
            return JsonResponse({'result': '', 'error' : item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET, PUT AND DELETE one item
@api_view(['GET', 'PUT', 'DELETE'])
def downtimeType_detail(request, pk):

    try:
        item = DowntimeType.objects.get(pk=pk)

        if request.method == 'GET':
            item_serializer = DowntimeTypeSerializer(item)
            return JsonResponse({'result': item_serializer.data, 'error' : ''}, status=HTTP_200_OK)

        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = DowntimeTypeSerializer(item, data=item_data, partial=True)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error' : ''})

            return JsonResponse({'result': '', 'error' : item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            item.delete()
            return JsonResponse(ResponseHttp(data='DowntimeType was deleted successfully').result, status=HTTP_204_NO_CONTENT)

    except DowntimeType.DoesNotExist:
        result = ResponseHttp(error='The downtimeType does not exist').result
        return JsonResponse(result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)