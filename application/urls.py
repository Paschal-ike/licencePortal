"""Accounts urls"""
from django.urls import path
from .views import NewApplicationCreateView, RenewalApplicationCreateView, ReissueApplicationCreateView

urlpatterns = [
    path('new/', NewApplicationCreateView.as_view(), name='new_application'),
    path('renewal/', RenewalApplicationCreateView.as_view(), name='renewal_application'),
    path('reissue/', ReissueApplicationCreateView.as_view(), name='reissue_application'),
    
]
