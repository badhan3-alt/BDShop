from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),  # store listing
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),  # product detail page
    path('search',views.search,name='search'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),

]
