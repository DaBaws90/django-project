from django.urls import path
from . import views
from .views import (
    HomeRestaurantPage, OrdersListPage, OrderDetailsPage, OrderCreatePage, OrderUpdatePage, OrderDeletaPage,
    PlaceListPage, PlaceDetailsPage, PlaceCreatePage
)
from django.views.generic import RedirectView

urlpatterns = [
    path('', HomeRestaurantPage.as_view(), name = "homeRestaurant"),
    path('pedidos/', OrdersListPage.as_view(), name = "ordersIndex"),
    path('pedidos/pedido/<int:pk>/', OrderDetailsPage.as_view(), name = "orderDetails"),
    path('pedidos/create/', OrderCreatePage.as_view(), name = "orderCreate"),
    path('pedidos/update/<int:pk>/', OrderUpdatePage.as_view(), name = "orderUpdate"),
    path('pedidos/delete/<int:pk>/', OrderDeletaPage.as_view(), name = "orderDelete"),
    path('lugares/', PlaceListPage.as_view(), name = "placesIndex"),
    path('lugares/lugar/<int:pk>/', PlaceDetailsPage.as_view(), name = "placeDetails"),
    path('lugares/create/', PlaceCreatePage.as_view(), name = "placeCreate"),
]
