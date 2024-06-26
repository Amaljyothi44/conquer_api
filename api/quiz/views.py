from rest_framework import generics, status
from .models import Quiz, Countdb, News, Reminder, Subquiz
from .serializers import QuizSerializer, CountSerializer,NewsSerializer, RemindSerializer,SubquizSerializer
from rest_framework.response import Response
from django.http import JsonResponse,HttpResponse
from datetime import datetime, timedelta
from django.views.decorators.csrf import csrf_exempt
import json, time, os, zipfile
import traceback
from django.core.serializers import serialize
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


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
    
#--sub quiz

class SubquizListCreateView(generics.ListCreateAPIView):
    queryset = Subquiz.objects.all()
    serializer_class = SubquizSerializer

class SubquizRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subquiz.objects.all()
    serializer_class = SubquizSerializer

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(
            instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        return Response(serializer.data)


class NewsList(generics.ListCreateAPIView):
    queryset = News.objects.all()
    serializer_class = NewsSerializer

    def create(self, request, *args, **kwargs):
        # Get the title from the request data
        new_title = request.data.get('title')
   
        # Check if a record with the same title already exists
        existing_news = News.objects.filter(title=new_title).first()

        if existing_news:
            # Return a response indicating that the record already exists
            return Response({'message': 'Record with this title already exists.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            if len(News.objects.all()) > 150 :
                news_del = News.objects.first()
                news_del.delete()
            count_object, created = Countdb.objects.get_or_create(dateAnswer=datetime.now().date())
            count_object.totalnews += 1
            count_object.save()
            # Continue with the normal creation process
            return super().create(request, *args, **kwargs)

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

class RemindList(generics.ListCreateAPIView):
    queryset = Reminder.objects.all()
    serializer_class = RemindSerializer

class RemindRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Reminder.objects.all()
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
        eli_leng = len(eligible_questions)
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
                'id': question_data.id,
                'eli_len' : eli_leng,
            }
            return JsonResponse(serialized_question)


REPETITION_INTERVALS = [0, 3, 5, 7, 10, 12, 15, 18, 20]

REPETITION_INTERVALS_REM = [0, 3, 3, 5, 5, 5, 7, 7, 7, 10]

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
                'remcount' : count_object.remcount,
                'newscount': count_object.newscount,
                'totalnews': count_object.totalnews,
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
    all_count = Countdb.objects.all()
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
    serialized_count = [
            {
                "id": counter.id,
                "mark": counter.mark,
                "count": counter.count,
                "dateAnswer": counter.dateAnswer.strftime("%Y-%m-%d")
            }
            for counter in all_count
        ]
    with open('upload.json', 'w', encoding='utf-8') as json_file:
        json.dump(serialized_questions, json_file,ensure_ascii=False, indent=2)
    
    with open('counter.json', 'w', encoding='utf-8') as json_file:
        json.dump(serialized_count, json_file,ensure_ascii=False, indent=2)
        
     # Create a zip file containing both JSON files
    zip_file_path = 'download_files.zip'
    with zipfile.ZipFile(zip_file_path, 'w') as zipf:
        zipf.write('upload.json', 'upload.json')
        zipf.write('counter.json', 'counter.json')

    try:
        # Open the zip file for reading
        with open(zip_file_path, 'rb') as zip_file:
            # Create an HTTP response with the content type for zip files and attachment for download
            response = HttpResponse(zip_file.read(), content_type='application/zip')
            response['Content-Disposition'] = 'attachment; filename="download_files.zip"'
            return response

    except FileNotFoundError:
        return JsonResponse({'error': 'File not found'}, status=404)

    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

    finally:
        # Clean up: remove temporary JSON files and the zip file
        os.remove('upload.json')
        os.remove('counter.json')
        os.remove(zip_file_path)

    
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
                
                existing_news = News.objects.filter(title=article_head).first()
                if not existing_news:
                    news, created = News.objects.get_or_create(title=article_head, defaults={'body': article_body, 'date': news_time})
                    count_object, created = Countdb.objects.get_or_create(dateAnswer=datetime.now().date())
                    count_object.totalnews += 1
                    count_object.save()
                    if not created:
                        news.body = article_body
                        news.date = news_time
                        news.save()
                        if len(News.objects.all()) > 150 :
                            news_del = News.objects.first()
                            news_del.delete()
                    
   
        time.sleep(1)
        
    

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
def get_next_reminder_question(request):
    if request.method == 'GET':
        all_questions = Reminder.objects.all()
        
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
        
        eli_leng = len(eligible_questions)
        if len(eligible_questions) > 0:
            next_quiz_number = get_next_eligible_question(
                eligible_questions_dict)
            if next_quiz_number is None:
                next_quiz_number = get_next_question_no(questions_dict)
        else:
            next_quiz_number = get_next_question_no(questions_dict)

        if next_quiz_number is None :
            serialized_question = {
                'body' : "Question",
                'answer': "Question \n\n Finished",
                'eli_len' : 0,
                'questionNumber':'End',
            }
            return JsonResponse(serialized_question)
        else: 
            question_data = eligible_questions_dict.get(
                next_quiz_number) or questions_dict.get(next_quiz_number)
            serialized_question = {
                'questionNumber': question_data.questionNumber,
                'body': question_data.body,
                'subject': question_data.subject,
                'answer': question_data.answer,
                'id': question_data.id,
                'eli_len' : eli_leng,
            }
            return JsonResponse(serialized_question)
        
@csrf_exempt
def update_reminder_repetition(request, quiz_id):
    try:
        if request.method == 'POST':
            remind = Reminder.objects.get(id=quiz_id)
            result = True
            count_object, created = Countdb.objects.get_or_create(dateAnswer=datetime.now().date())
            count_object.remcount+=1
            count_object.save()
            if result :
                repetition_delay = get_repetition_delay_rem(remind.nextRepetition)
                next_repetition_date = datetime.now() + timedelta(days=repetition_delay)
                remind.nextRepetition = repetition_delay
                remind.date = next_repetition_date.strftime('%Y-%m-%d')
                remind.save()
                
                return JsonResponse({'message': 'Success'})
            else:
                return JsonResponse({'message': 'some error'})
        
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status=500)
    
def news_update(request):
    if request.method == 'GET':
        news = News.objects.all()
        sort_news = news.order_by('id')


@csrf_exempt
def next_news(request):
    if request.method == 'GET':
        # Retrieve the Count object for the given date
        news = News.objects.first()
        news_len = len(News.objects.all())
        if news is None:
            serialized_question = {
                'body': "Question Finished",
            }
            return JsonResponse(serialized_question)
        else :
            response_data = {
                'id': news.id,
                'title': news.title,
                'body' : news.body, 
                'date' : news.date,
                'news_len' : news_len
           }
        return JsonResponse(response_data)
    
    elif request.method == 'POST':
        count_object, created = Countdb.objects.get_or_create(dateAnswer=datetime.now().date())
        count_object.newscount += 1
        count_object.save()
        news_del = News.objects.first()
        news_del.delete()
        
        return JsonResponse({'message': 'Success'})
    
def conqure(request):
    return render(request, 'main.html')


@csrf_exempt
def reminder_update(request):
    try:
        if request.method == 'POST':
            
            body_unicode = request.body.decode('utf-8')
            body_data = json.loads(body_unicode)
            print([body_data])
            qs = len(Reminder.objects.all())

            remainder_ob, create = Reminder.objects.get_or_create(
                questionNumber= qs + 1,
                defaults={
                    'body': body_data.get('body'),
                    'answer': body_data.get('answer'),
                    'nextRepetition': 0,
                    
                    'subject': body_data.get('subject'),
                    'date': datetime.now().date(),
                }
            )
            return JsonResponse({'message': 'Success'})
    
    except Exception as e:
        traceback.print_exc()
        return JsonResponse({'message': str(e)}, status=500)       
    

#sub- quiz
@csrf_exempt
def get_sub_next_question(request):
    if request.method == 'GET':
        all_questions = Subquiz.objects.all()
    
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
        eli_leng = len(eligible_questions)
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
                'id': question_data.id,
                'eli_len' : eli_leng,
            }
            return JsonResponse(serialized_question)
        
@csrf_exempt
def update_sub_repetition(request, quiz_id):
    try:
        if request.method == 'POST':
            quiz = Subquiz.objects.get(id=quiz_id)
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