from django.contrib import admin
from django.urls import path,include
from pratice.views import hello,add

urlpatterns = [
    path('hello/',hello),
    path('add',add),
]
