from django.contrib import admin
from django.urls import path,include
from order_api import views

urlpatterns = [
    path('all_orders/', views.all_orders),
    path('id_order/<number_id>',views.id_order),
    path('create_user/',views.create_user),
    path('update_order/<order_id>',views.get_location)
]
