from rest_framework import generics
from .models import Quiz, Countdb, News, Remind
from .serializers import QuizSerializer, CountSerializer,NewsSerializer, RemindSerializer
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json, time
import traceback
from django.core.serializers import serialize
import requests
from bs4 import BeautifulSoup

class QuizListCreateView(generics.ListCreateAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer


class QuizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class NewsList(generics.ListAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

class NewsRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)

class RemindList(generics.ListAPIView):
    queryset = Remind.objects.all()
    serializer_class = RemindSerializer

class RemindRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Remind.objects.all()
    serializer_class = RemindSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


def is_question_due(question):
    
    next_repetition_date = datetime.strptime(
        str(question.date), '%Y-%m-%d') 
    return datetime.now() >= next_repetition_date


def get_next_eligible_question(eligible_questions_dict):
    for x in eligible_questions_dict:
        question_data = eligible_questions_dict[x]
        if is_question_due(question_data):
            print(x)
            return x
    return None


def get_next_question_no(questions_dict):
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
      
        sorted_quiz_data = filtered_quiz_data.order_by(
            'date', 'questionNumber')
       
        questions_dict = {
            item.questionNumber: item for item in sorted_quiz_data}
        
        # Use Django's filter to get eligible and sorted questions
        eligible_questions = all_questions.filter(
            nextRepetition__gt=0,
            date__lte=datetime.now().date()
        ).order_by('date', 'questionNumber')
        
        eligible_questions_dict = {
            item.questionNumber: item for item in eligible_questions}
       
        if len(eligible_questions) > 0:
            next_quiz_number = get_next_eligible_question(
                eligible_questions_dict)
            if next_quiz_number is None:
                next_quiz_number = get_next_question_no(questions_dict)
        else:
            next_quiz_number = get_next_question_no(questions_dict)

        if next_quiz_number is None:
            return JsonResponse({'message': 'No eligible questions found'})
        else:
            question_data = eligible_questions_dict.get(
                next_quiz_number) or questions_dict.get(next_quiz_number)
            serialized_question = {
                'questionNumber': question_data.questionNumber,
                'subject': question_data.subject,
                'question': question_data.question,
                'options': question_data.options,
                'correctOption': question_data.correctOption,
                'link': question_data.link,
                'id': question_data.id
            }
            return JsonResponse(serialized_question)


REPETITION_INTERVALS = [0, 3, 5, 7, 10, 12]

REPETITION_INTERVALS_REM = [0, 3, 3, 5, 5, 5, 7, 7, 7, 10, 10, 10, 12]

def get_repetition_delay(last_repetition):
  
    if last_repetition == REPETITION_INTERVALS[-1]:
        return REPETITION_INTERVALS[-1]
    else:
        increment = REPETITION_INTERVALS.index(last_repetition)
        return REPETITION_INTERVALS[increment + 1]
    
def get_repetition_delay_rem(last_repetition):
  
    if last_repetition == REPETITION_INTERVALS_REM[-1]:
        return REPETITION_INTERVALS_REM[-1]
    else:
        increment = REPETITION_INTERVALS_REM.index(last_repetition)
        return REPETITION_INTERVALS_REM[increment + 1]


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

        # Replace with your actual response
        return JsonResponse({'message': 'Success'})
    except Quiz.DoesNotExist:
        return JsonResponse({'message': 'Quiz not found'}, status=404)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status=500)


class dbcount(generics.ListCreateAPIView):
    queryset = Countdb.objects.all()
    serializer_class = CountSerializer


class dbcountupdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Countdb.objects.all()
    serializer_class = CountSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


@csrf_exempt
def count_and_mark(request):
    try:

        if request.method == 'GET':
            # Retrieve the Count object for the given date
            count_object, created = Countdb.objects.get_or_create(
                dateAnswer=datetime.now().date())

            # Prepare the response
            response_data = {
                'dateAnswer': count_object.dateAnswer.strftime('%Y-%m-%d'),
                'count': count_object.count,
                'mark': count_object.mark,
            }
           
            return JsonResponse(response_data)

        elif request.method == 'POST':
            count_object, created = Countdb.objects.get_or_create(
                dateAnswer=datetime.now().date())
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            result = body_data.get('result', None)

            if result is not None:
                count_object.count += 1

                if result:
                    count_object.mark += 1

                count_object.save()

                return JsonResponse({'message': 'count Success'})
            else:
                return JsonResponse({'message': 'Result is required'}, status=400)

    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status=500)
    
@csrf_exempt
def download_json(request):
    
    all_questions = Quiz.objects.all()

    serialized_questions = [
            {
                "id": quiz.id,
                "question": quiz.question,
                "options": quiz.options,
                "nextRepetition": quiz.nextRepetition,
                "questionNumber": quiz.questionNumber,
                "subject": quiz.subject,
                "link": quiz.link,
                "correctOption": quiz.correctOption,
                "date": quiz.date.strftime("%Y-%m-%d")
            }
            for quiz in all_questions
        ]
    with open('upload.json', 'w', encoding='utf-8') as json_file:
        json.dump(serialized_questions, json_file,ensure_ascii=False, indent=2)
        
    file_path = 'upload.json'

    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Load the JSON content
            json_content = json.load(file)

        # Convert the JSON content to a pretty printed string
        json_string = json.dumps(json_content, indent=4)

        # Create an HTTP response with the content type for JSON and attachment for download
        response = HttpResponse(json_string, content_type='application/json')
        response['Content-Disposition'] = 'attachment; filename="upload.json"'
        return response

    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def scrape_article_content(request):
    url = scrape_the_hindu_news()
    while True:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            news_time = soup.find('p', class_='publish-time').text.strip()
            article_head = soup.find('h1', class_='title').text.strip()
            article_content = soup.find('div', class_='articlebodycontent col-xl-9 col-lg-12 col-md-12 col-sm-12 col-12')

            if article_content:
                for unwanted_section in article_content.find_all(class_=lambda x: x in ['comments', 'share', 'related-topics']):
                    unwanted_section.decompose()
                article_body = "\n\n".join([p.get_text() for p in article_content.find_all('p')])
                
                news, created = News.objects.get_or_create(title=article_head, defaults={'body': article_body, 'date': datetime.now()})

                if not created:
                    news.body = article_body
                    current_datetime = datetime.now()
                    news.date = current_datetime.strftime("%Y-%m-%d %H:%M")
                    news.save()

            # Move the sleep outside of the if block to make sure it's executed in every iteration
            time.sleep(1)
        else:
            # Add some logging or handling for unsuccessful requests
            print(f"Failed to retrieve data. Status code: {response.status_code}")
    

def scrape_the_hindu_news():
    url = 'https://www.thehindu.com/latest-news/'
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        first_link = soup.select_one('h3 > a')
        if first_link:
            return first_link['href']  
    return None

@csrf_exempt
def get_next_remainder_question(request):
    if request.method == 'GET':
        all_questions = Remind.objects.all()
        # Use Django's filter to get eligible and sorted questions
        filtered_quiz_data = all_questions.filter(nextRepetition__lt=1)
        sorted_quiz_data = filtered_quiz_data.order_by(
            'date', 'questionNumber')

        questions_dict = {
            item.questionNumber: item for item in sorted_quiz_data}

        # Use Django's filter to get eligible and sorted questions
        eligible_questions = all_questions.filter(
            nextRepetition__gt=0,
            date__lte=datetime.now().date()
        ).order_by('date', 'questionNumber')
    
        eligible_questions_dict = {
            item.questionNumber: item for item in eligible_questions}

        if len(eligible_questions) > 0:
            next_quiz_number = get_next_eligible_question(
                eligible_questions_dict)
            if next_quiz_number is None:
                next_quiz_number = get_next_question_no(questions_dict)
        else:
            next_quiz_number = get_next_question_no(questions_dict)

        if next_quiz_number is None:
            serialized_question = {
                'body': "Question Finished",
            }
            return JsonResponse(serialized_question)
        else:
            question_data = eligible_questions_dict.get(
                next_quiz_number) or questions_dict.get(next_quiz_number)
            serialized_question = {
                'questionNumber': question_data.questionNumber,
                'body': question_data.body,
                'answer': question_data.answer,
                'id': question_data.id
            }
            return JsonResponse(serialized_question)
        
@csrf_exempt
def update_remainder_repetition(request, quiz_id):
    try:
        if request.method == 'POST':
            remind = Remind.objects.get(id=quiz_id)
            result = True
            if result :
                repetition_delay = get_repetition_delay_rem(remind.nextRepetition)
                next_repetition_date = datetime.now() + timedelta(days=repetition_delay)
                remind.nextRepetition = repetition_delay
                remind.date = next_repetition_date.strftime('%Y-%m-%d')
                remind.save()
            

        # Replace with your actual response
        return JsonResponse({'message': 'Success'})
    except Quiz.DoesNotExist:
        return JsonResponse({'message': 'Quiz not found'}, status=404)
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status=500)