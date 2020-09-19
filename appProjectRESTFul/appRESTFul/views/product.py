from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.db.models import Q

from ..models import ProductsProcesses
from ..serializers import ProductsProcessesSerializer
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


@api_view(['GET', 'POST', 'DELETE'])
def product_list(request):

    try:

        if request.method == 'GET':
            items = list(ProductsProcesses.objects.all())

            items_serializer = ProductsProcessesSerializer(items, many=True)

            return JsonResponse(items_serializer.data, safe=False, status=HTTP_200_OK)

        elif request.method == 'POST':
            item_data = JSONParser().parse(request)
            item_serializer = ProductsProcessesSerializer(data=item_data)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error': ''}, status=HTTP_201_CREATED)
            return JsonResponse({'result': '', 'error': item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            count = ProductsProcesses.objects.all().delete()
            return JsonResponse(ResponseHttp(data='{0} products were deleted successfully!'.format(count[0])).result, status=HTTP_204_NO_CONTENT)

    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET, PUT AND DELETE one item
@api_view(['GET', 'PUT', 'DELETE'])
def product_detail(request, pk):

    try:
        item = ProductsProcesses.objects.get(pk=pk)

        if request.method == 'GET':
            item_serializer = ProductsProcessesSerializer(item)
            return JsonResponse({'result': item_serializer.data, 'error': ''}, status=HTTP_200_OK)

        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = ProductsProcessesSerializer(
                item, data=item_data, partial=True)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error': ''})

            return JsonResponse({'result': '', 'error': item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            item.delete()
            return JsonResponse(ResponseHttp(data='Product was deleted successfully').result, status=HTTP_204_NO_CONTENT)

    except ProductsProcesses.DoesNotExist:
        result = ResponseHttp(error='The machine does not exist').result
        return JsonResponse(result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET an item by condition
@ api_view(['POST'])
def product_filter(request):

    items = list(ProductsProcesses.objects.select_related('machines').filter(Q(machines__name__icontains=request.data.get('name') or '')).select_related('items').filter(Q(items__item_description__icontains=request.data.get('description') or '')))

    try:
        if request.method == 'POST':
            item_serializer=ProductsProcessesSerializer(items, many = True)
            return JsonResponse(item_serializer.data, safe = False)

    except ProductsProcesses.DoesNotExist:
        return JsonResponse(ResponseHttp(error='Product does not exist').result, status = HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status = HTTP_500_INTERNAL_SERVER_ERROR)
