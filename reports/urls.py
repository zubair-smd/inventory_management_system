from django.urls import path
from . import views

urlpatterns = [
    path('report/', views.report_view, name='report_list'),
]
