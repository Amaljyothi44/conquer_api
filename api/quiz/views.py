from rest_framework import generics
from .models import Quiz, Countdb
from .serializers import QuizSerializer,CountSerializer
from rest_framework.response import Response
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json, traceback


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
                'link' : question_data.link,
                'id': question_data.id
            }
            return JsonResponse(serialized_question)
        
REPETITION_INTERVALS = [0, 3, 5, 7, 10, 12]
def get_repetition_delay(last_repetition):
    print("working repeter delay")
    if last_repetition == REPETITION_INTERVALS[-1]:
        return REPETITION_INTERVALS[-1]
    else:
        increment = REPETITION_INTERVALS.index(last_repetition)
        return REPETITION_INTERVALS[increment + 1]
           
@csrf_exempt    
def update_repetition(request, quiz_id):
    try:
        if request.method == 'POST':
            quiz = Quiz.objects.get(id=quiz_id)
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            result = body_data.get('result', None)
            if result == True:
                repetition_delay = get_repetition_delay(quiz.nextRepetition)
                next_repetition_date = datetime.now() + timedelta(days=repetition_delay)
                quiz.nextRepetition = repetition_delay 
                quiz.date = next_repetition_date.strftime('%Y-%m-%d')
                quiz.save()
            else:
                next_repetition_date = datetime.now() + timedelta(days=3)
                quiz.nextRepetition = 3
                quiz.date = next_repetition_date.strftime('%Y-%m-%d')
                quiz.save()
        
        return JsonResponse({'message': 'Success'})  # Replace with your actual response
    except Quiz.DoesNotExist:
        return JsonResponse({'message': 'Quiz not found'}, status=404)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status=500)
        
class dbcount(generics.ListCreateAPIView):
    queryset = Countdb.objects.all()
    serializer_class = CountSerializer



        

