from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('place_order/', views.place_order, name='place_order'),
    path('payment/<str:order_number>/', views.payment_view, name='payment'),
    path('checkout/', views.checkout, name='checkout'),
    path('cod_order/', views.cod_order, name='cod_order'),
    path('process_bkash/', views.process_bkash, name='process_bkash'),
    path('order-complete/<str:order_number>/', views.order_complete, name='order_complete'),


]
