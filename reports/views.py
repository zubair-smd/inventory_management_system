from django.shortcuts import render
from django.db.models import Sum, Count,  F
from inventory.models import Inventory, Order

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

    context = {
        'total_stock': total_stock,
        'low_stock_items': low_stock_items,
        'total_orders': total_orders,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'total_sales': total_sales,
        'total_items_sold': total_items_sold,
    }
    return render(request, 'reports/reports.html', context)