from django.urls import path
from . import views
from .views import HomePage, CustomerListPage, CustomerDetailsPage, CustomerCreatePage

urlpatterns = [
    path('', HomePage.as_view(), name = "home"),
    path('clientes/', CustomerListPage.as_view(), name = "customersIndex"),
    path('<int:id>/<slug:slug>/', CustomerDetailsPage.as_view(), name = "customerDetails"),
    # path('create/', CustomerCreatePage.as_view(), name = "customersCreate"),
    path('create/', views.create_user, name = "customersCreate"),
    path('reviews/', views.listReviews, name = "reviewsIndex"),
    path('contact/', views.contactUs, name = "contact"),
]
