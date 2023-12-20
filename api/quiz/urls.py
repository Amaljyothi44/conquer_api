# urls.py
from django.urls import path
from .views import QuizListCreateView, QuizRetrieveUpdateDestroyView, get_next_question,update_repetition,dbcount,count_and_mark,dbcountupdate,download_json

urlpatterns = [
    path('quiz/', QuizListCreateView.as_view(), name='quiz-list-create'),
    path('quiz/<int:pk>/', QuizRetrieveUpdateDestroyView.as_view(), name='quiz-retrieve-update-destroy'),
    path('get-next-question/', get_next_question, name='get_next_question'),
    path('update-repetition/<int:quiz_id>/',update_repetition, name ='update_repetition'),
    path('count/',dbcount.as_view(), name ='dbcount'),
    path('count/<int:pk>/',dbcountupdate.as_view(), name ='dbcountupdate'),
    path('count-mark/',count_and_mark,name='count_and_mark'),
    path('download/', download_json, name='download_json'),
]
