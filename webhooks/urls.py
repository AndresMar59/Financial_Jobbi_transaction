from django.urls import path
from .views import brex_webhook_receiver

urlpatterns = [
    path('brex-receiver/', brex_webhook_receiver, name='brex_webhook'),
    
]