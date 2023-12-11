# urls.py
from django.urls import path
from .views import QuizListCreateView, QuizRetrieveUpdateDestroyView, get_next_question,update_repetition,dbcount

urlpatterns = [
    path('quiz/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quiz/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-retrieve-update-destroy'),
    path('get-next-question/', get_next_question, name='get_next_question'),
    path('update-repetition/<int:quiz_id>/',update_repetition, name ='update_repetition'),
    path('count/',dbcount.as_view(), name ='dbcount'),
]
