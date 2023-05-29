from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.core.mail import send_mail

from products.models import Order

# It's stated in the help attribute, but this command will send a reminder to all users that have a pending payment to do.
class Command(BaseCommand):
    help = "It sends an email to remind all users that they have a pending payment to complete in less than 24hs"
    
    def handle(self, *args, **kwargs):
        today = datetime.now()
        orders = Order.objects.filter(
            is_paid=False,
            creation_date__gte=today-timedelta(hours=24),
            #creation_date__lte=today-timedelta(hours=1)
        ).exclude(mercado_link=None)
        
        for order in orders:
            message = "Hi " + order.buyer.get_full_name() + "!! \nYou have a pending order to pay with the following products:\n"
            for product in order.products.all():
                message += "Name: " + product.name
            message += "\nYou can complete the payment here: " + order.mercado_link + "\nThank you!"

            send_mail(
                subject="Reminder! You have an order to complete",
                message=message,
                from_email=None,
                recipient_list=[order.buyer.email],
                fail_silently=False
                )