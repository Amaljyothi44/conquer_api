
from rest_framework import serializers
from .models import Quiz,Count

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Count
        fields = '__all__'
