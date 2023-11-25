from django.db import models

class Quiz(models.Model):
    question = models.TextField()
    options = models.JSONField()  
    nextRepetition = models.IntegerField()  
    questionNumber = models.IntegerField()  
    subject = models.TextField()
    link = models.URLField()  
    correctOption = models.IntegerField()  
    date = models.DateField() 
