from django.urls import path
from .views import PaymentId, nextpay_callback

urlpatterns = [
    path('nextpay-payemnt', PaymentId.as_view()),
    path('callback', nextpay_callback)
]
