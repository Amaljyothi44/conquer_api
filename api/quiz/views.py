from rest_framework import generics
from .models import Quiz
from .serializers import QuizSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime, timedelta

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


def is_question_due(question):
    next_repetition_date = datetime.strptime(str(question.date), '%Y-%m-%d') + timedelta(days=question.nextRepetition)
    return datetime.now() >= next_repetition_date

def get_next_eligible_question(eligible_questions_dict):
    for x in eligible_questions_dict:
        question_data = eligible_questions_dict[x]
        if is_question_due(question_data):
            return x
    return None

def get_next_question(questions_dict):
    for quiz_number in questions_dict:
        question_data = questions_dict[quiz_number]
        if is_question_due(question_data):
            return quiz_number
    return None

def get_next_question(request):
    if request.method == 'GET':
        all_questions = Quiz.objects.all()

        # Use Django's filter to get eligible and sorted questions
        filtered_quiz_data = all_questions.filter(nextRepetition__lt=1)
        sorted_quiz_data = filtered_quiz_data.order_by('date', 'questionNumber')

        questions_dict = {item.questionNumber: item for item in sorted_quiz_data}

        # Use Django's filter to get eligible and sorted questions
        eligible_questions = all_questions.filter(
            nextRepetition__gt=0,
            date__lte=datetime.now().date()
        ).order_by('date', 'questionNumber')

        eligible_questions_dict = {item.questionNumber: item for item in eligible_questions}

        if len(eligible_questions) > 0:
            next_quiz_number = get_next_eligible_question(eligible_questions_dict)
            if next_quiz_number is None:
                next_quiz_number = get_next_question(questions_dict)
        else:
            next_quiz_number = get_next_question(questions_dict)

        if next_quiz_number is None:
            return JsonResponse({'message': 'No eligible questions found'})
        else:
            question_data = eligible_questions_dict.get(next_quiz_number) or questions_dict.get(next_quiz_number)
            serialized_question = {
                'questionNumber': question_data.questionNumber,
                'subject' : question_data.subject,
                'question': question_data.question,
                'options' : question_data.options,
                'correctOption' : question_data.correctOption,
                'link' : question_data.link
            }
            return JsonResponse(serialized_question)
        

