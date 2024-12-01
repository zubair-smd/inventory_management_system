from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from .forms import SignUpForm, LoginForm
from django.contrib.auth.decorators import login_required
from inventory.models import Product, Inventory, Order, Notification
from django.db.models import F
from django.db.models import Sum


from django.shortcuts import render
from inventory.models import Inventory, Order, Product
# User Signup
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect
from django.http import JsonResponse

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            # Save the form (this will automatically hash the password)
            form.save()
            
            # Optionally, you can redirect the user to the login page after successful registration
            #return redirect('dashboard')  # Adjust 'login' to match your actual login URL name

            # Or, you can return a JsonResponse with a success message if you want to keep the AJAX pattern
            # return JsonResponse({'message': 'User created successfully'}, status=201)
        # If form is invalid, return the errors in the response
        return JsonResponse({'errors': form.errors.as_json()}, status=400)
    else:
        # Initialize an empty form for GET requests
        form = UserCreationForm()
    
    # Render the signup page with the form
    return render(request, 'authentication/signup.html', {'form': form})


# User Login
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('dashboard') 
                #return JsonResponse({'message': 'Login successful'}, status=200)
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
        return JsonResponse({'errors': form.errors}, status=400)
    else:
        form = LoginForm()
    return render(request, 'authentication/login.html', {'form': form})

# User Logout
def user_logout(request):
    logout(request)
    return redirect('login')
# Dashboard view







def dashboard(request):
    # Orders statistics
    to_be_packed = Order.objects.filter(status='To Be Packed').count()
    to_be_shipped = Order.objects.filter(status='Completed').count()  # To Be Shipped = Completed Orders
    to_be_delivered = Order.objects.filter(status='To Be Delivered').count()
    to_be_invoiced = Order.objects.filter(status='Pending').count()  # To Be Invoiced = Pending Orders
    pending_orders = Order.objects.filter(status='Pending').count()
    completed_orders = Order.objects.filter(status='Completed').count()

    # Inventory statistics
    total_stock = Inventory.objects.aggregate(total=Sum('stock_level'))['total'] or 0  # Default to 0 if no data
    low_stock_items = Inventory.objects.filter(stock_level__lt=10).count()  # Adjust threshold if needed
    sufficient_stock = max(total_stock - low_stock_items, 0)  # Ensure no negative values are shown

    # Product statistics
    total_products = Product.objects.count()  # Total number of products
    low_stock_items_list = Product.objects.filter(quantity__lt=3)[:1]  # Get top 3 low-stock products
    low_stock_count1 = Product.objects.filter(quantity__lt=4).count()  # Total count of low-stock products
    sufficient_stock1 = Product.objects.filter(quantity__gte=50).count()  # Count of sufficient-stock products

    # Context for template
    context = {
        'to_be_packed': to_be_packed,
        'to_be_shipped': to_be_shipped,  # Completed orders
        'to_be_invoiced': to_be_invoiced,  # Pending orders
        'to_be_delivered': to_be_delivered,
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'sufficient_stock': sufficient_stock,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_products': total_products,
        'low_stock_items_list': low_stock_items_list,  # Pass the top 3 low-stock products to the template
        'low_stock_count1': low_stock_count1,  # Total count of low-stock products
        'sufficient_stock1': sufficient_stock1,  # Total count of sufficient-stock products
    }

    return render(request, 'authentication/dashboard.html', context)




def purchase_list(request):
    # Logic for fetching and displaying purchases
    return render(request, 'authentication/purchase_list.html')
