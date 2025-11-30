from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('Payment/<str:order_number>/', views.Payment, name='Payment'),
    path('checkout/', views.checkout, name='checkout')
    
]
