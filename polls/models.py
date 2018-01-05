"""
    Django application models
"""
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone


@python_2_unicode_compatible  # support python 2
class Question(models.Model):
    """
    Class Question stores question with its published date and time
    """
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.question_text

    def was_published_recently(self):
        """
        Checks whether the question is published within 1 day or not
        :return:
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now


@python_2_unicode_compatible  # support python 2
class Choice(models.Model):
    """
    Class Choice stores textvalue and number of votes
    Associated with Question using Foreign Key
    """
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
