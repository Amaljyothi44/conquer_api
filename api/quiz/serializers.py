
from rest_framework import serializers
from .models import Quiz,Countdb,News, Reminder, Subquiz

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countdb
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'

class RemindSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reminder
        fields = '__all__'

class SubquizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subquiz
        fields = '__all__'