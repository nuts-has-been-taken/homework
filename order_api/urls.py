from django.contrib import admin
from django.urls import path,include
from order_api import views

urlpatterns = [
    path('all_orders/', views.all_orders),
    path('id_order/<order_id>',views.id_order),
    path('loc_order/<order_id>',views.loc_order)
]
