from django.db import models
import datetime
from django.utils import timezone

# Each model has a number of class variables, each of which represents a database field in the model
class Question(models.Model):
    question_text = models.CharField(max_length=200) # Database will use these names as column names
    pub_date = models.DateTimeField('date published')
    def __str__(self):
        return self.question_text
    # It’s important to add __str__() methods to your models, not only for your own convenience when dealing with the interactive prompt, but also because objects’ representations are used throughout Django’s automatically-generated admin.
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)
    
class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE) # The foreign key tells django each choice is related to a single question
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0) # default value is 0
    def __str__(self):
        return self.choice_text