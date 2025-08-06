from django.db import transaction
from .models import Order, Product
import logging
from django.contrib.auth.models import User
from .email_utils import send_order_email


logger = logging.getLogger(__name__)

# Payment Successful 
@transaction.atomic
def handle_payment_success(session_data):
    metadata = session_data.get('metadata', {})
    user_id = metadata.get('user_id')
    product_id = metadata.get('product_id')
    payment_intent_id = session_data.get('payment_intent')
    if not all([user_id, product_id, payment_intent_id]):
        logger.error(f"Error: Required metadata not found from session {session_data.get('id')}.")

    try:
        user = User.objects.get(pk=user_id)
        product = Product.objects.get(id=product_id)

        order, created = Order.objects.update_or_create(
            payment_intent_id = payment_intent_id,
            defaults = {
                'user': user,
                'product':product,
                'is_paid':True,
                'is_refunded':False
            }
        )
        
        if created:
            logger.info(f"New order #{order.id} created.")
        else:
            logger.info(f"New order #{order.id} updated.")
        
        send_order_email(user, order, 'Your order has been successful!', './order_success_email.html')
    except User.DoesNotExist:
        logger.error(f" Critical Error: User ID {user_id} not found in the database.")
    
    except Product.DoesNotExist:
        logger.error(f'Critical Error: Product ID {product_id} not found in the database.')
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}', exc_info=True)


@transaction.atomic
def handle_payment_failure(session):
    pass
@transaction.atomic
def handle_session_expired(session):
    pass
@transaction.atomic
def handle_refund(charge):
    pass 