from django.urls import path
from .views import RegisterView, ProductListView, ProductDetailView, CreateCheckoutSessionView, StripeWebhookView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail view'),
    path('product/<int:pk>/create-checkout-session/', CreateCheckoutSessionView.as_view(),name='create-checkout-session'),
    path('stripe-webhook/', StripeWebhookView.as_view(), name='stripe-webhook' ),
]