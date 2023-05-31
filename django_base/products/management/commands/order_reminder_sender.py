from django.core.management.base import BaseCommand

from products.cron import reminder_sender

class Command(BaseCommand):
    help = "It sends an email to remind all users that they have a pending payment to complete in less than 24hs"
    
    def handle(self, *args, **kwargs):
        reminder_sender()