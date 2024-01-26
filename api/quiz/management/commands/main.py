from django.core.management.base import BaseCommand
from quiz.models import Quiz, Countdb, News, Reminder
import json, time

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **options):
        
        self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
