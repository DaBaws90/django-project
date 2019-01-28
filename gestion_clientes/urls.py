from django.urls import path
from . import views
from .views import (
    HomePage, CustomerListPage, CustomerDetailsPage, CustomerDeletePage, 
    ReviewsListPage, ReviewDetailsPage, ReviewsCreatePage
)

urlpatterns = [
    path('', HomePage.as_view(), name = "home"),
    path('clientes/', CustomerListPage.as_view(), name = "customersIndex"),
    path('clientes/<int:pk>/<slug:slug>/', CustomerDetailsPage.as_view(), name = "customerDetails"),
    # path('create/', CustomerCreatePage.as_view(), name = "customersCreate"),
    path('create/', views.create_user, name = "customersCreate"),
    path('update/<int:pk>/', views.update_user2, name = "customersUpdate"),
    path('delete/<int:pk>/', CustomerDeletePage.as_view(), name = "customersDelete"),
    path('reviews/', ReviewsListPage.as_view(), name = "reviewsIndex"),
    path('reviews/<int:pk>/', ReviewDetailsPage.as_view(), name = "reviewDetails"),
    path('reviews/create/', ReviewsCreatePage.as_view(), name = "reviewsCreate"),
    path('contact/', views.contactUs, name = "contact"),
]
