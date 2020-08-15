from django.http.response import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status

from ..models  import Item
from ..serializers import ItemsSerializer
from rest_framework.decorators import api_view


@api_view(['GET', 'POST', 'DELETE'])
def item_list(request):

    if request.method == 'GET':
        items = Item.objects.all()

        items_serializer = ItemsSerializer(items, many=True)
        return JsonResponse(items_serializer.data, safe=False)

    elif request.method == 'POST':
        item_data = JSONParser().parse(request)
        item_serializer = ItemsSerializer(data=item_data)

        if item_serializer.is_valid():
            item_serializer.save()
            return JsonResponse(item_serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        count = Item.objects.all().delete()
        return JsonResponse({'message': '{0} Items were deleted successfully!'.format(count[0])}, status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
def item_detail(request, pk):

    try:
        item = Item.objects.get(pk=pk)

        if request.method == 'GET':
            item_serializer = ItemsSerializer(item)
            return JsonResponse(item_serializer.data)

        elif request.method == 'PUT':
            item_data = JSONParser().parse(request)
            item_serializer = ItemsSerializer(item, data=item_data)
                        
            if item_serializer.is_valid():
                item_serializer.save()
                return JsonResponse(item_serializer.data)
            
            return JsonResponse(item_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == 'DELETE': 
            item.delete()
            return JsonResponse({'message': 'Tutorial was deleted successfully!'}, status=status.HTTP_204_NO_CONTENT)

    except Item.DoesNotExist:
        return JsonResponse({'message': 'The tutorial does not exist'}, status=status.HTTP_404_NOT_FOUND)
