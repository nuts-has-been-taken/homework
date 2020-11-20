from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser
from order_api.serializers import OrderSerializer,CustomerSerializer,DeliverySerializer
from MyToDoList.models import Order,Customer,Delivery
from mongoengine.errors import ValidationError
import math
import requests

@api_view(['POST'])
def create_user(request):
    user_data = JSONParser().parse(request)
    if user_data['species'] == 'customer' :
        customer_serializer = CustomerSerializer(data=user_data)
        if customer_serializer.is_valid():
            customer_serializer.save()
            return JsonResponse(customer_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(customer_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    elif user_data['species'] == 'delivery' :
        delivery_serializer = DeliverySerializer(data=user_data)
        if delivery_serializer.is_valid():
            delivery_serializer.save()
            return JsonResponse(delivery_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(delivery_serializer.errors,status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET' , 'DELETE'])
def all_orders(request):
    if request.method == 'GET':
        all_order = Order.objects.all()
        all_order_serializer = OrderSerializer(all_order, many=True)
        return JsonResponse(all_order_serializer.data, status=status.HTTP_200_OK, safe=False)
    if request.method == 'DELETE':
        count = Order.objects.all().delete()
        return JsonResponse({'message':'{} Orders were deleted successfully!'.format(count)},status=status.HTTP_204_NO_CONTENT)

@api_view(['GET','POST','DELETE'])
def id_order(request,number_id):
    #新增訂單的同時，將order的訂單id加入顧客名下，此時number_id為顧客的id
    if request.method == 'POST':
        the_order = JSONParser().parse(request)
        order_serializer = OrderSerializer(data=the_order)
        if order_serializer.is_valid():
            try:
                customer_number = Customer.objects.get(id=number_id)
            except Customer.DoesNotExist:
                return JsonResponse({'message': 'The Customer does not exist'},status=status.HTTP_404_NOT_FOUND)
            except ValidationError:
                return JsonResponse({'message': 'The type of id is not correct'},status=status.HTTP_400_BAD_REQUEST)
            order_serializer.save()
            customer_number.orders.append(str(order_serializer["id"]))
            update_data = {
                "_id":customer_number.id,
                "species":customer_number.species,
                "name":customer_number.name,
                "gender":customer_number.gender,
                "phone_number":customer_number.phone_number,
                "email":customer_number.email,
                "password":customer_number.password,
                "orders":customer_number.orders
            }
            customer_serializer = CustomerSerializer(customer_number,data=update_data)
            if customer_serializer.is_valid():
                print('saving....')
                customer_serializer.save()
            return JsonResponse(order_serializer.data,status=status.HTTP_201_CREATED)
        return JsonResponse(order_serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    #GET DEL為查詢 刪除訂單，此時number_id為訂單的id
    try:
        order_number = Order.objects.get(id=number_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'},status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return JsonResponse({'message': 'The type of id is not correct'},status=status.HTTP_400_BAD_REQUEST)
    
    if request.method == 'GET': 
        order_serializer = OrderSerializer(order_number)
        return JsonResponse(order_serializer.data)
    
    if request.method == 'DELETE':
        order_number.delete()
        return JsonResponse({'message': 'The order was deleted successfully!'},status=status.HTTP_204_NO_CONTENT)


@api_view(['GET'])
def get_location(request,order_id):
    try:
        number = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'},status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return JsonResponse({'message': 'The type of id is not correct'},status=status.HTTP_400_BAD_REQUEST)
    a = number.driver_lat
    x,y = a[0],a[1]
    b = number.lat
    nx,ny = b[0],b[1]
    far = math.sqrt((x-nx)**2 + (y-ny)**2)
    if  far <= 5 :
        return JsonResponse({'message': 'Your order is here'})
    else :
        return JsonResponse({'message': 'Your order is far from '+ str(far) +' meter'})
@api_view(['PUT'])
def delivery_update_loc(request,order_id):
    try:
        number = Order.objects.get(id=order_id)
    except Order.DoesNotExist:
        return JsonResponse({'message': 'The order does not exist'},status=status.HTTP_404_NOT_FOUND)
    except ValidationError:
        return JsonResponse({'message': 'The type of id is not correct'},status=status.HTTP_400_BAD_REQUEST)
    the_order = JSONParser().parse(request)
    order_serializer = OrderSerializer(number,data=the_order)
    if order_serializer.is_valid():
        order_serializer.save()
        return JsonResponse(order_serializer.data,status=status.HTTP_201_CREATED)