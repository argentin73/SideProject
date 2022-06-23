from django.urls import path
from .api import init_paypal, create_order, finalize_invoice, stripe_webhook
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('paypal', init_paypal),
    path('create-order', create_order),
    path('finalize-invoice', finalize_invoice),
    path('stripe-webhook', csrf_exempt(stripe_webhook), name="stripe-webhook"),
]