from django.db import models

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
    def __unicode__(self):
        return self.choice    
        
from lino import dd

class Polls(dd.Table):
    model = Poll
    
class Choices(dd.Table):
    model = Choice
        
class ChoicesByPoll(Choices):
    master_key = 'poll'