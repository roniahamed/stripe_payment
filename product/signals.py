from django.dispatch import Signal 

order_successfully_processed = Signal()
payment_failed = Signal()
payment_refunded = Signal()
