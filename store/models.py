from django.db import models
from django.utils.text import slugify
import random
import string
from category.models import Category  # fixed import


# Function to generate order numbers
def generate_order_number():
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))


# Product model
class Product(models.Model):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name='products'
    )
    name = models.CharField(max_length=150)
    slug = models.SlugField(max_length=160, unique=True, blank=True)
    short_description = models.TextField(blank=True, null=True)  # <-- fix for existing DB
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    available = models.BooleanField(default=True)
    image = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # Automatically generate slug on save
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variations')
    variation_category = models.CharField(max_length=100)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.variation_category}: {self.variation_value}"