from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = "home"),
    path('clientes/', views.listCustomers, name = "customersIndex"),
    path('cliente/<int:customer_id>', views.customerDetails, name = "customerDetails"),
    path('reviews/', views.listReviews, name = "reviewsIndex"),
    path('contact/', views.contactUs, name = "contact"),
]
