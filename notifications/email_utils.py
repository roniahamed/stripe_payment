from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings

def send_order_email(user, order, subject, template_name):

    try:
        context = {
            'username':user.username,
            'order_id':order.id,
            'product_name':order.product.name,
            'order_price':order.product.price,
        }
        message = render_to_string(template_name, context)
        send_mail (subject, message, settings.DEFAULT_FROM_EMAIL,[user.email], html_message=message, fail_silently=False)
    except Exception as e:
        pass
    