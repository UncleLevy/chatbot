#users/urls.py
from django.urls import path
from .views import RegisterView, LoginView, TokenBalanceView
from rest_framework_simplejwt.views import ( TokenObtainPairView)

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    # path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token_balance/', TokenBalanceView.as_view(), name='token_balance'),
]