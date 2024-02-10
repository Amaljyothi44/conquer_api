# Create a new file inside your Django app, e.g., myapp/management/commands/load_data.py

from django.core.management.base import BaseCommand
from quiz.models import Quiz, Countdb, News, Reminder
import json, time

# class Command(BaseCommand):
#     help = 'Load data from JSON file into the database'

#     def handle(self, *args, **options):
#         json_file_path = 'quiz/management/commands/counter.json'

#         with open(json_file_path, 'r' , encoding='utf-8') as json_file:
#             data = json.load(json_file)

#         start_total_time = time.time()
#         for item in data:
#             start_time = time.time()
            
#             Countdb.objects.create(**item)
#             elapsed_time = time.time() - start_time
#             print(f" added successfully. Time: {elapsed_time:.6f} seconds")
            
#         total_time = time.time() - start_total_time
#         print(f"Total time for uploading all : {total_time:.6f} seconds")
#         self.stdout.write(self.style.SUCCESS('Data loaded successfully'))

class Command(BaseCommand):
    help = 'Load data from JSON file into the database'

    def handle(self, *args, **options):
      all_questions = Quiz.objects.all()
      filtered_quiz_data = all_questions.filter(nextRepetition=10)
      sorted_quiz_data = filtered_quiz_data.order_by(
            'date', 'questionNumber')

    #   for item in sorted_quiz_data:
    #      print(str(item.questionNumber))
      print(f"Leng : {len(filtered_quiz_data)}")
      self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
