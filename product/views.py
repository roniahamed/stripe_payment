from django.contrib.auth.models import User
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework import generics
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

stripe.api_key = settings.api_key = settings.STRIPE_SECRET_KEY

