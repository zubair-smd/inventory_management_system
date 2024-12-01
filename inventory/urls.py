from django.urls import path
from . import views

urlpatterns = [
    # Supplier URLs
    path('suppliers/', views.supplier_list, name='supplier_list'),
    path('suppliers/add/', views.supplier_create, name='supplier_create'),
    path('suppliers/<int:pk>/edit/', views.supplier_update, name='supplier_update'),

    # Other URLs (Products, Inventory, Orders) can go here
     # Products
    path('products/', views.product_list, name='product_list'),
    path('products/add/', views.product_create, name='product_create'),
    path('products/<int:pk>/edit/', views.product_update, name='product_update'),
    path('products/<int:pk>/delete/', views.product_delete, name='product_delete'),

    # Inventory
    path('inventory/', views.inventory_list, name='inventory_list'),
    path('inventory/<int:pk>/edit/', views.inventory_update, name='inventory_update'),

    # Orders
    path('orders/', views.order_list, name='order_list'),
    path('orders/add/', views.order_create, name='order_create'),
    path('orders/<int:pk>/edit/', views.order_update, name='order_update'),
    
    path('notifications/', views.notification_list, name='notification_list'),
    path('notifications/<int:pk>/read/', views.mark_notification_read, name='mark_notification_read'),
    
    path('purchases/', views.purchase_list, name='purchase_list'),
    path('report/', views.report_view, name='report'),
    path('documents/', views.document_list, name='document_list'),
    path('reportpdf/', views.generate_report_pdf, name='generate_report_pdf'),
    path('generate_report_pdf/', views.generate_report_pdf, name='generate_report_pdf'),
    
]
