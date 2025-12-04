from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
    path('search',views.search,name='search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

]
