from rest_framework_mongoengine.serializers import DocumentSerializer
from MyToDoList.models import Order
class OrderSerializer(DocumentSerializer):
    class Meta:
        model = Order
        fields = '__all__'