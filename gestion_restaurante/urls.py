from django.urls import path
from . import views
from .views import (
    HomeRestaurantPage, OrdersListPage, OrderDetailsPage, OrderCreatePage, OrderUpdatePage, OrderDeletaPage,
    PlaceListPage, PlaceDetailsPage, PlaceCreatePage, PlaceUpdatePage, PlaceDeletePage, About,
    ProductListPage, ProductDetailsPage, ProductCreatePage, ProductUpdatePage, ProductDeletePage,
    RestaurantListPage, RestaurantDetailsPage, RestaurantCreatePage, RestaurantUpdatePage, RestaurantDeletePage
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
    path('lugares/update/<int:pk>/', PlaceUpdatePage.as_view(), name = "placeUpdate"),
    path('lugares/delete/<int:pk>/', PlaceDeletePage.as_view(), name = "placeDelete"),
    path('productos/', ProductListPage.as_view(), name = "productsIndex"),
    path('productos/producto/<int:pk>/', ProductDetailsPage.as_view(), name = "productDetails"),
    path('productos/create', ProductCreatePage.as_view(), name = "productCreate"),
    path('productos/update/<int:pk>/', ProductUpdatePage.as_view(), name = "productUpdate"),
    path('productos/delete/<int:pk>/', ProductDeletePage.as_view(), name = "productDelete"),
    path('restaurantes/', RestaurantListPage.as_view(), name = "restaurantsIndex"),
    path('restaurantes/restaurante/<int:pk>/', RestaurantDetailsPage.as_view(), name = "restaurantDetails"),
    path('restaurantes/create/', RestaurantCreatePage.as_view(), name = "restaurantCreate"),
    path('restaurantes/update/<int:pk>/', RestaurantUpdatePage.as_view(), name = "restaurantUpdate"),
    path('restaurantes/delete/<int:pk>/', RestaurantDeletePage.as_view(), name = "restaurantDelete"),
    path('about/', About.as_view(), name = "about"),
]
# urlpatterns += place_crud.get_url_patterns()
