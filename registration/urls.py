from django.urls import path
from . import views
from django.views.generic import RedirectView
from .views import SignIn
from django.contrib.auth.views import login, logout

urlpatterns = [
    path('signup/', views.signup, name = "register"),
    # path('signin/', SignIn.as_view(), name = "login"),
    path('signin/', SignIn.as_view(), name = "login"),
    path('profile/', views.profile_update, name = "profile"),
    path('logout/', logout),
]
