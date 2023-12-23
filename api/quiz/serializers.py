
from rest_framework import serializers
from .models import Quiz,Countdb,News, Remind

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

class RemindSerializer(serializers.ModelField):
    class Meta:
        model = Remind
        field = '__all__'
