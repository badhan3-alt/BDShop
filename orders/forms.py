from django import forms
from .models import Order

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'first_name', 'last_name', 'phone', 'email',
            'address_line_1', 'address_line_2',
            'country', 'state', 'city', 'order_note'
        ]

        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'phone': forms.TextInput(attrs={'placeholder': 'Phone'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email'}),
            'address_line_1': forms.TextInput(attrs={'placeholder': 'Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'placeholder': 'Address Line 2'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'state': forms.TextInput(attrs={'placeholder': 'State'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'order_note': forms.Textarea(attrs={'placeholder': 'Order Note', 'rows': 3}),
        }

        labels = {
            'first_name': 'First Name',
            'last_name': 'Last Name',
            'phone': 'Phone',
            'email': 'Email',
            'address_line_1': 'Address Line 1',
            'address_line_2': 'Address Line 2',
            'country': 'Country',
            'state': 'State',
            'city': 'City',
            'order_note': 'Order Note',
        }
