from django.dispatch import receiver
from product.signals import order_successfully_processed
from .email_utils import send_order_email

@receiver(order_successfully_processed)
def handle_order_email_notification(sender, order, created, **kwargs):
    if created:
        subject = 'Your new order has been successful!'
    else:
        subject = 'Your order has been updated!'
    
    send_order_email(user=order.user,order=order, subject=subject, template_name='./order_success_email.html')