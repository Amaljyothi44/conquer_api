from django.db import models

class Quiz(models.Model):
    question = models.TextField()
    options = models.JSONField()  
    nextRepetition = models.IntegerField()  
    questionNumber = models.IntegerField()  
    subject = models.TextField()
    link = models.URLField(null=True, blank=True)
    correctOption = models.IntegerField()  
    date = models.DateField() 

class Countdb(models.Model):
    mark =  models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    remcount = models.IntegerField(default=0)
    newscount = models.IntegerField(default=0)
    totalnews = models.IntegerField(default=0)
    dateAnswer = models.DateField(unique=True) 

    def __str__(self):
        return f'{self.dateAnswer} -mark:{self.mark}'

class News(models.Model):
    title = models.TextField()
    body = models.JSONField()  
    date = models.TextField()

class Reminder(models.Model):
    body = models.TextField()
    answer = models.TextField()
    nextRepetition = models.IntegerField()  
    questionNumber = models.IntegerField()  
    date = models.DateField(null=True, blank=True) 
    subject = models.TextField()
    