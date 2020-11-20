from rest_framework_mongoengine.serializers import DocumentSerializer
from MyToDoList.models import Order,Customer,Delivery
class OrderSerializer(DocumentSerializer):
    class Meta:
        model = Order
        fields = '__all__'
class CustomerSerializer(DocumentSerializer):
    class Meta:
        model = Customer
        fields = '__all__'
class DeliverySerializer(DocumentSerializer):
    class Meta:
        model = Delivery
        fields = '__all__'