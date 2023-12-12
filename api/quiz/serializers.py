
from rest_framework import serializers
from .models import Quiz,Countdb

class QuizSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quiz
        fields = '__all__'

class CountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Countdb
        fields = '__all__'
