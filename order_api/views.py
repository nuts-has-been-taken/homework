from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from order_api.serializers import OrderSerializer
from MyToDoList.models import Order
from mongoengine.errors import ValidationError
import requests

@api_view(['GET', 'POST', 'DELETE'])
def all_orders(request):
    if request.method == 'GET':
        all_order = Order.objects.all()
        all_order_serializer = OrderSerializer(all_order, many=True)
        return JsonResponse(all_order_serializer.data, status=status.HTTP_200_OK, safe=False)

    if request.method == 'POST':
        the_order = JSONParser().parse(request)
        order_serializer = OrderSerializer(data=the_order)
        if order_serializer.is_valid():
            order_serializer.save()
            return JsonResponse(order_serializer.data,status=status.HTTP_201_CREATED)

    if request.method == 'DELETE':
        count = Order.objects.all().delete()
        return JsonResponse(
            {'message': '{} Orders were deleted successfully!'.format(count)},status=status.HTTP_204_NO_CONTENT)
    
    return JsonResponse(order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        
@api_view(['GET','DELETE'])
def id_order(request,order_id):
    try:
        number = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'},status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return JsonResponse({'message': 'The type of id is not correct'},status=status.HTTP_400_BAD_REQUEST)
    if request.method == 'GET': 
        order_serializer = OrderSerializer(number)
        return JsonResponse(order_serializer.data)
    if request.method == 'DELETE':
        number.delete()
        return JsonResponse({'message': 'The order was deleted successfully!'},status=status.HTTP_204_NO_CONTENT)






@api_view(['GET'])
def loc_order(request,order_id):
    try:
        number = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'},status=status.HTTP_404_NOT_FOUND)
    a=JSONParser().parse(request)
    lng = a['lng']
    lat = a['lat']
    order_serializer = OrderSerializer(number)
    return JsonResponse(order_serializer.data)