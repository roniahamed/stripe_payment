from django.db import transaction
from .models import Order, Product
import logging
from django.contrib.auth.models import User
from .signals import order_successfully_processed

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
        
        order_successfully_processed.send(sender=Order, order=order, created = created)
    except User.DoesNotExist:
        logger.error(f" Critical Error: User ID {user_id} not found in the database.")
    
    except Product.DoesNotExist:
        logger.error(f'Critical Error: Product ID {product_id} not found in the database.')
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}', exc_info=True)


# handle payment failure
@transaction.atomic
def handle_payment_failure(session_data):
    """
    Handler for the 'checkout.session.async_payment_failed' event.
    Logs the reason for the failed payment and notifies the user via email.
    """
    session_id = session_data.get('id')
    logger.error(f'Asynchronous payment failed for checkout session {session_id}')

    metadata = session_data.get('metadata', {})
    user_id = metadata.get('user_id')
    product_id = metadata.get('product_id')

    try:
        user = User.objects.get(pk = user_id)
        products = Product.objects.get(pk=product_id)

        # Creating an "order-like" object for the email template
        # because at this stage no order has been created in the database.

        class TempOrder:
            id = 'Incomplete'
            product = products

        # send_order_email(user, TempOrder(), 'Your payment has failed', './payment_failure_email.html')

    except User.DoesNotExist:
        logger.error(f'User ID {user_id} not found while sending payment failure notification.')
    except Product.DoesNotExist:
        logger.error(f'Product ID {product_id} not found while sending payment failure notification.')
    except Exception as e:
        logger.error(f'An error occurred while sending the payment failure notification')

@transaction.atomic
def handle_session_expired(session):
    pass


# Handle refunds 


@transaction.atomic
def handle_refund(refund_data):
    payment_intent_id = refund_data.get('payment_intent')
    logger.info(f'Refund Webhook received: {payment_intent_id}')

    if not payment_intent_id:
        logger.error(f'Error: Could not find payment_intent_id in refund data')
        return 

    try:
        order = Order.objects.get(payment_intent_id=payment_intent_id)

        # If the order is already marked as refunded, nothing to do.
        # Prevents duplicate webhook handling.
        if order.is_refunded:
            logger.warning(f'Order : {order.id} is already marked as refunded. Webhook ignored.')
            return 
        order.is_refunded = True
        order.save()
        logger.info(f'Order #{order.id} successfully marked as refunded.')

        # send_order_email(order.user, order, 'Your order has been refunded', './refund_processed_email.html' )
    except Order.DoesNotExist:
        logger.error(f'Critical: No order found for payment_intent_id {payment_intent_id}.')    
    except Exception as e:
        logger.error(f'An unexpected error occurred while handling the refund: {e}', exc_info=True)
        
        

    