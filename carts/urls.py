from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
app_name = 'carts' 
urlpatterns = [
    path('', views.cart, name='cart'),
    path('add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('delete/<int:product_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
