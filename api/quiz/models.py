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
    dateAnswer = models.DateField(unique=True) 
    def __str__(self):
        return f'{self.dateAnswer} -mark:{self.mark} - Count: {self.dcount}'

class News(models.Model):
    title = models.TextField()
    body = models.JSONField()  
    date = models.DateTimeField()

class Remind(models.Model):
    body = models.TextField()
    answer = models.TextField()
    nextRepetition = models.IntegerField()  
    questionNumber = models.IntegerField()  
    date = models.DateTimeField() 

    