from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view

from ..models import Item
from ..serializers import ItemsSerializer
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
def item_list(request):

    try:

        if request.method == 'GET':
            items = list(Item.objects.all())
            items_serializer = ItemsSerializer(items, many=True)
            
            return JsonResponse(items_serializer.data, safe=False, status=HTTP_200_OK)

        elif request.method == 'POST':
            item_data = JSONParser().parse(request)
            item_serializer = ItemsSerializer(data=item_data)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error' : ''}, status=HTTP_201_CREATED)
            return JsonResponse({'result': '', 'error' : item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            count = Item.objects.all().delete()
            return JsonResponse(ResponseHttp(data='{0} items were deleted successfully!'.format(count[0])).result, status=HTTP_204_NO_CONTENT)

    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)


# GET, PUT AND DELETE one item
@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):

    try:
        item = Item.objects.get(pk=pk)

        if request.method == 'GET':
            item_serializer = ItemsSerializer(item)
            return JsonResponse({'result': item_serializer.data, 'error' : ''}, status=HTTP_200_OK)

        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = ItemsSerializer(item, data=item_data, partial=True)

            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse({'result': item_serializer.data, 'error' : ''})

            return JsonResponse({'result': '', 'error' : item_serializer.errors}, status=HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE':
            item.delete()
            return JsonResponse(ResponseHttp(data='Item was deleted successfully').result, status=HTTP_204_NO_CONTENT)

    except Item.DoesNotExist:
        result = ResponseHttp(error='The item does not exist').result
        return JsonResponse(result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)
    

# GET an item by condition
@ api_view(['POST'])
def item_filter(request):
    
    kwargs = {
        '{0}__{1}'.format('statusId', 'exact'): request.data.get('statusId') or 1,
        '{0}__{1}'.format('description', 'icontains'): request.data.get('description') or ''
    }
    
    items = list(Item.objects.filter(**kwargs))

    try:
        if request.method == 'POST':
            item_serializer = ItemsSerializer(items, many=True)
            return JsonResponse(item_serializer.data, safe=False)

    except Item.DoesNotExist:
        return JsonResponse(ResponseHttp(error='The item does not exist').result, status=HTTP_404_NOT_FOUND)
    except Exception as error:
        return JsonResponse(ResponseHttp(error=str(error)).result, status=HTTP_500_INTERNAL_SERVER_ERROR)
