
# Register your models here.
from django.contrib import admin
from .models import Category, Product




# Product admin
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'stock', 'available', 'created_at', 'updated_at')
    list_filter = ('available', 'category', 'created_at', 'updated_at')
    list_editable = ('price', 'stock', 'available')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')
    ordering = ('name',)