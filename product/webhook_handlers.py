from django.db import transaction
from .models import Order

@transaction.atomic
def handle_payment_success(session):
    pass

def handle_payment_failure(session):
    pass

def handle_session_expired(session):
    pass

def handle_refund(charge):
    pass 