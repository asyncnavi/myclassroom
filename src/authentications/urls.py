from django.urls import path
from .views import *
from django.contrib.auth import logout

urlpatterns = [
    path('', auth_view, name="auth"),
    path('signup', signup_view, name="signup"),
    path('logout', logout_view, name="logout"),
    path('login', login_view, name="login"),
]
