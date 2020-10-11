from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from order_api.serializers import OrderSerializer
from MyToDoList.models import Order

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
        count = order.objects.all().delete()
        return JsonResponse(
            {'message': '{} Orders were deleted successfully!'.format(count)},status=status.HTTP_204_NO_CONTENT)
    
    return JsonResponse(order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
        
@api_view(['GET'])
def id_order(request,order_id):
    try:
        number = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'},status=status.HTTP_404_NOT_FOUND)     
    order_serializer = OrderSerializer(number)
    return JsonResponse(order_serializer.data)
