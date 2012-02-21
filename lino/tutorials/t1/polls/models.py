from django.db import models
from lino import dd

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField()
    
    def __unicode__(self):
        return self.choice    
        
class Polls(dd.Table):
    model = Poll
    detail_template = """
    id question pub_date
    polls.ChoicesByPoll
    """
    
    
class Choices(dd.Table):
    model = Choice
        
class ChoicesByPoll(Choices):
    master_key = 'poll'