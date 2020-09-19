from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from django.db.models import Q

from ..models import ProductionStatus
from ..serializers import ProductionStatusSerializer
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
def productionStatus_list(request):

    try:

        if request.method == 'GET':
            items = list(ProductionStatus.objects.all())
            items_serializer = ProductionStatusSerializer(items, many=True)

            return JsonResponse(items_serializer.data, safe=False, status=HTTP_200_OK)

        elif request.method == 'POST':
            item_data = JSONParser().parse(request)
            item_serializer = ProductionStatusSerializer(data=item_data)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error': ''}, status=HTTP_201_CREATED)
            return JsonResponse({'result': '', 'error': item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET, PUT AND DELETE one item
@api_view(['GET', 'PUT', 'DELETE'])
def productionStatus_detail(request, pk):

    try:
        item = ProductionStatus.objects.get(pk=pk)

        if request.method == 'GET':
            item_serializer = ProductionStatusSerializer(item)
            return JsonResponse({'result': item_serializer.data, 'error': ''}, status=HTTP_200_OK)

        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = ProductionStatusSerializer(
                item, data=item_data, partial=True)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error': ''})

            return JsonResponse({'result': '', 'error': item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            item.delete()
            return JsonResponse(ResponseHttp(data='Production status was deleted successfully').result, status=HTTP_204_NO_CONTENT)

    except ProductionStatus.DoesNotExist:
        result = ResponseHttp(
            error='The production status does not exist').result
        return JsonResponse(result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)

# GET an item by condition


@ api_view(['POST'])
def productionStatus_filter(request):

    kwargs = {
        '{0}__{1}'.format('statusId', 'exact'): request.data.get('statusId') or 1,
        '{0}__{1}'.format('description', 'icontains'): request.data.get('description') or ''
    }
    
    items = list(ProductionStatus.objects.filter(**kwargs))

    try:
        if request.method == 'POST':
            item_serializer = ProductionStatusSerializer(items, many=True)
            return JsonResponse(item_serializer.data, safe=False)

    except ProductionStatus.DoesNotExist:
        return JsonResponse(ResponseHttp(error='The item does not exist').result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)
