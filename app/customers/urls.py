from django.contrib import admin
from django.urls import path, include
from . import views

app_name = 'customers'

urlpatterns = [
    path('customers/', views.CustomerTable.as_view(), name='customers'),
    path('customers/add/', views.CustomerCreate.as_view(), name='customer_add'),
    path('customers/add/<str:id>/', views.CustomerUpdate.as_view(), name='customer_update'),
    path('customers/delete/<int:pk>/', views.CustomerDelete.as_view(), name='customer_delete'),

    path('customerprice/delete/<int:pk>/', views.CustomerPriceDelete.as_view(), name='customerprice_delete'),
]
