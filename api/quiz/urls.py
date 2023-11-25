# urls.py
from django.urls import path
from .views import QuizListCreateView, QuizRetrieveUpdateDestroyView

urlpatterns = [
    path('quiz/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quiz/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-retrieve-update-destroy'),
]
