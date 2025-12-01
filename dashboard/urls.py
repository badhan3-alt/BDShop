from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('my_orders/', views.my_orders, name='my_orders'),
    path('transactions/', views.transactions, name='transactions'),
    path('return_requests/', views.return_requests, name='return_requests'),
    path('settings/', views.settings_view, name='settings'),
    path('my_selling_items/', views.my_selling_items, name='my_selling_items'),
    path('received_orders/', views.received_orders, name='received_orders'),
]
