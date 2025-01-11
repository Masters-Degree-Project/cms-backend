from django.core.management.base import BaseCommand
from api.worker import start_worker

class Command(BaseCommand):
    help = 'Starts the Redis queue worker'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting worker...'))
        start_worker() 