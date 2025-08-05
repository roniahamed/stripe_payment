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
                ]
            )
            mode = 'payment',
            success_url = 'http://localhost:8000/success/',
            cancel_url = 'http://localhost:8000/cancel/',
            metadata = {
                'user_id': request.user.id,
                'product_id':product.id
            }

            return Response({'checkout_url':checkout_session})
        except Product.DoesNotExist:
            return Response({'error':'Product not found'})


class StripeWebhookView(APIView):
    permission_classes = [AllowAny]

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
            

