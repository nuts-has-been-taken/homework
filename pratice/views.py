from rest_framework.decorators import api_view
from django.http.response import JsonResponse
from rest_framework import status
from rest_framework.parsers import JSONParser

@api_view(['GET'])
def hello(request):
    return JsonResponse({'message': 'hello'},status=status.HTTP_200_OK)


@api_view(['POST'])
def add(request):
    a=JSONParser().parse(request)
    x=a['x']
    y=a['y']
    return JsonResponse({'answer': x+y},status=status.HTTP_200_OK)
    