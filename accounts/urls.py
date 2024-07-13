"""Accounts Urls"""
from django.urls import path
from .views import SignUpView, CustomTokenObtainPairView, TokenRefreshView, LogoutView

urlpatterns = [
    path('signup/', SignUpView.as_view(), name='signup'),
    path('login/', CustomTokenObtainPairView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
