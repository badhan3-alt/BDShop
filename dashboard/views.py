from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from orders.models import Order, OrderProduct
from .models import Transaction, ReturnRequest, UserSettings, ReceivedOrder

@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-id')
    return render(request, 'dashboard/my_orders.html', {'orders': orders})

@login_required
def transactions(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/transactions.html', {'transactions': transactions})

@login_required
def return_requests(request):
    returns = ReturnRequest.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'dashboard/return_requests.html', {'returns': returns})

@login_required
def settings_view(request):
    settings_obj, created = UserSettings.objects.get_or_create(user=request.user)
    if request.method == 'POST':
        preferences = request.POST.get('preferences')
        settings_obj.preferences = {'preferences': preferences}
        settings_obj.save()
        return redirect('dashboard:settings')
    return render(request, 'dashboard/settings.html', {'settings': settings_obj})

@login_required
def my_selling_items(request):
    received_orders = ReceivedOrder.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'dashboard/my_selling_items.html', {'received_orders': received_orders})

@login_required
def received_orders(request):
    orders = ReceivedOrder.objects.filter(seller=request.user).order_by('-created_at')
    return render(request, 'dashboard/received_orders.html', {'orders': orders})


@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    return render(request, 'accounts/dashboard.html', {'orders': orders})
