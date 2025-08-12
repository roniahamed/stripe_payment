from django.views.generic import TemplateView
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProductSerializer, OrderSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics, status
from django.conf import settings

# stripe
import stripe
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Order
from . import webhook_handlers

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class ProductDetailView(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

class PaymentSuccessView(TemplateView):
    template_name = 'success.html'

class PaymentCancelView(TemplateView):
    template_name = 'cancel.html'

stripe.api_key = settings.api_key = settings.STRIPE_SECRET_KEY

class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = self.kwargs.get('pk')
        try:
            product = Product.objects.get(pk=product_id)
            checkout_session = stripe.checkout.Session.create(
                payment_method_types = ['card'],
                line_items = [{
                    'price_data':{
                        'currency':'usd',
                        'product_data': {'name':product.name,},
                        'unit_amount':int(product.price * 100),
                    },
                    'quantity':1,
            }
                ],
            
            mode = 'payment',
            success_url = 'http://localhost:8002/api/success/',
            cancel_url = 'http://localhost:8002/api/cancel/',
            metadata = {
                'user_id': request.user.id,
                'product_id':product.id
            }
            )

            return Response({'checkout_url':checkout_session})
        except Product.DoesNotExist:
            return Response({'error':'Product not found'})


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

    event_handler_map = {
        'checkout.session.completed': webhook_handlers.handle_payment_success,
        'checkout.session.expired': webhook_handlers.handle_session_expired,
        'checkout.session.async_payment_failed': webhook_handlers.handle_payment_failure,
        'charge.refunded': webhook_handlers.handle_refund,
    }

    def post(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META['HTTP_STRIPE_SIGNATURE']
        event = None

        try:
            event = stripe.Webhook.construct_event(payload, sig_header, settings.STRIPE_WEBHOOK_SECRET)
        except ValueError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        except stripe.error.SignatureVerificationError as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        
        handler = self.event_handler_map.get(event['type'])

        if handler:
            try:
                handler(event['data']['object'])
            except Exception as e:
                print(f'Error handling event {event['type']}: {e}')
                return Response({'error':'Internal server error in handler.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        return Response(status=status.HTTP_200_OK)





