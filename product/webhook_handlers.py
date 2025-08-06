from django.db import transaction
from .models import Order, Product
import logging
from django.contrib.auth.models import User
from .email_utils import send_order_email


logger = logging.getLogger(__name__)

@transaction.atomic
def handle_payment_success(session):
    
@transaction.atomic
def handle_payment_failure(session):
    pass
@transaction.atomic
def handle_session_expired(session):
    pass
@transaction.atomic
def handle_refund(charge):
    pass 