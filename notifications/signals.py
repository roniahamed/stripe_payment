from django.dispatch import receiver
from product.signals import order_successfully_processed, payment_failed, payment_refunded
from .email_utils import send_order_email

@receiver(order_successfully_processed)
def handle_order_email_notification(sender, order, created, **kwargs):
    if created:
        subject = 'Your new order has been successful!'
    else:
        subject = 'Your order has been updated!'
    
    send_order_email(user=order.user,order=order, subject=subject, template_name='./order_success_email.html')

@receiver(payment_refunded)
def handle_payment_refunded(sender, order, **kwargs):
    subject = 'Your order has been refunded!'
    send_order_email(user=order.user, order=order, subject=subject, template_name='./refund_processed_email.html')

@receiver(payment_failed)
def handle_payment_failed(sender, user, order, **kwargs):
        subject = 'Your order has been Failed!'
        send_order_email(user=user, order=order, subject=subject, template_name='./payment_failure_email.html')