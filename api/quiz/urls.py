# urls.py
from django.urls import path
from .views import QuizListCreateView, QuizRetrieveUpdateDestroyView, get_next_question

urlpatterns = [
    path('quiz/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quiz/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-retrieve-update-destroy'),
    path('get-next-question/', get_next_question, name='get_next_question'),
]
