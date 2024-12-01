from django.shortcuts import render, get_object_or_404, redirect
from .models import Supplier
from django.shortcuts import render, redirect
from .models import Notification
from django.db.models import Sum, Count
from .models import Inventory, Order
from django.db.models import F
from .models import Product, Inventory, Supplier, Order
from django.template.loader import render_to_string
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.utils.safestring import mark_safe 
import os
# List all suppliers
def supplier_list(request):
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/supplier_list.html', {'suppliers': suppliers})

# Create a new supplier
def supplier_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        contact_email = request.POST['contact_email']
        phone_number = request.POST['phone_number']
        Supplier.objects.create(name=name, contact_email=contact_email, phone_number=phone_number)
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_form.html')

# Update an existing supplier
def supplier_update(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    if request.method == 'POST':
        supplier.name = request.POST['name']
        supplier.contact_email = request.POST['contact_email']
        supplier.phone_number = request.POST['phone_number']
        supplier.save()
        return redirect('supplier_list')
    return render(request, 'inventory/supplier_form.html', {'supplier': supplier})





# List all products
def product_list(request):
    products = Product.objects.all()
    return render(request, 'inventory/product_list.html', {'products': products})

# Create a new product
def product_create(request):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        price = request.POST['price']
        supplier_id = request.POST['supplier']
        supplier = Supplier.objects.get(id=supplier_id)
        product = Product.objects.create(name=name, description=description, price=price, supplier=supplier)
        Inventory.objects.create(product=product, stock_level=0, reorder_threshold=10)
        return redirect('product_list')
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/product_form.html', {'suppliers': suppliers})

# Update a product
def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.name = request.POST['name']
        product.description = request.POST['description']
        product.price = request.POST['price']
        product.supplier = Supplier.objects.get(id=request.POST['supplier'])
        product.save()
        return redirect('product_list')
    suppliers = Supplier.objects.all()
    return render(request, 'inventory/product_form.html', {'product': product, 'suppliers': suppliers})

# Delete a product
def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.delete()
    return redirect('product_list')


# List all inventory items
def inventory_list(request):
    inventory_items = Inventory.objects.all()
    return render(request, 'inventory/inventory_list.html', {'inventory_items': inventory_items})

# Update stock level
def inventory_update(request, pk):
    inventory_item = get_object_or_404(Inventory, pk=pk)
    if request.method == 'POST':
        inventory_item.stock_level = request.POST['stock_level']
        inventory_item.reorder_threshold = request.POST['reorder_threshold']
        inventory_item.save()
        return redirect('inventory_list')
    return render(request, 'inventory/inventory_form.html', {'inventory_item': inventory_item})



# List all orders
def order_list(request):
    orders = Order.objects.all()
    return render(request, 'inventory/order_list.html', {'orders': orders})

# Create a new order
def order_create(request):
    if request.method == 'POST':
        product_id = request.POST['product']
        quantity = request.POST['quantity']
        product = Product.objects.get(id=product_id)
        Order.objects.create(product=product, quantity=quantity, status='Pending')
        return redirect('order_list')
    products = Product.objects.all()
    return render(request, 'inventory/order_form.html', {'products': products})

# Update an order status
def order_update(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        order.status = request.POST['status']
        order.save()
        return redirect('order_list')
    return render(request, 'inventory/order_form.html', {'order': order})




# List all notifications
def notification_list(request):
    notifications = Notification.objects.all().order_by('-created_at')  # Show newest first
    return render(request, 'inventory/notification_list.html', {'notifications': notifications})

# Mark a notification as read
def mark_notification_read(request, pk):
    notification = Notification.objects.get(pk=pk)
    notification.is_read = True
    notification.save()
    return redirect('notification_list')



def purchase_list(request):
    # Logic for fetching and displaying purchases
    return render(request, 'inventory/purchase_list.html')


def document_list(request):
    # Logic for displaying documents
    return render(request, 'app_name/document_list.html')  # Replace 'app_name' with the correct app name



from django.db.models import Sum, Count, F
from django.shortcuts import render
from .models import Inventory, Order

import json
from django.db.models import F, Sum

def report_view(request):
    # Inventory Levels Report
    total_stock = Inventory.objects.aggregate(total=Sum('stock_level'))['total'] or 0
    low_stock_items = Inventory.objects.filter(stock_level__lte=F('reorder_threshold')).count()

    # Order Statuses Report
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    completed_orders = Order.objects.filter(status='Completed').count()

    # Sales and Performance Metrics
    total_sales = Order.objects.annotate(order_total=F('product__price') * F('quantity')) \
                                .aggregate(total=Sum('order_total'))['total'] or 0
    total_items_sold = Order.objects.aggregate(total=Sum('quantity'))['total'] or 0

    # Prepare data for charts
    order_status_data = mark_safe([pending_orders, completed_orders])
    stock_status_data = mark_safe([low_stock_items, total_stock - low_stock_items])

    context = {
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
        'order_status_data': order_status_data,
        'stock_status_data': stock_status_data,
    }
    return render(request, 'inventory/reports.html', context)


def generate_report_pdf(request):
    # Calculate report data
    total_stock = Inventory.objects.aggregate(total=Sum('stock_level'))['total'] or 0
    low_stock_items = Inventory.objects.filter(stock_level__lte=F('reorder_threshold')).count()
    total_orders = Order.objects.count()
    pending_orders = Order.objects.filter(status='Pending').count()
    completed_orders = Order.objects.filter(status='Completed').count()
    total_sales = Order.objects.annotate(order_total=F('product__price') * F('quantity')).aggregate(total=Sum('order_total'))['total'] or 0
    total_items_sold = Order.objects.aggregate(total=Sum('quantity'))['total'] or 0

    # Context for the template
    context = {
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
    }

    # Render the HTML template with context
    html_content = render_to_string('inventory/reports_pdf.html', context)

    # Create the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Inventory_Report.pdf"'

    # Generate PDF
    pisa_status = pisa.CreatePDF(html_content, dest=response)

    # Handle errors
    if pisa_status.err:
        return HttpResponse('Error generating PDF', status=500)
    
    return response