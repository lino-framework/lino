import cgi
import datetime
from django.db import models
from django.conf import settings
from lino import dd
from lino.utils import babel

class Poll(dd.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateField('date published',blank=True,null=True)
    #~ pub_date = models.DateTimeField('date published',auto_now_add=True)
    
    def __unicode__(self):
        return self.question
        
    def was_published_today(self):
        return self.pub_date == datetime.date.today()        
        #~ return self.pub_date.date() == datetime.date.today()        
        
class Choice(dd.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    @dd.action(show_in_workflow=True)
    def vote(self,ar,**kw):
        self.votes += 1
        self.save()
        kw.update(refresh=True)
        kw.update(message="Thank you for voting")
        kw.update(alert="Voted!")
        return ar.success_response(**kw)
        
    def __unicode__(self):
        return self.choice    
        
        


class Polls(dd.Table):
    model = Poll
    
    detail_template = """
    id question pub_date
    polls.ChoicesByPoll
    """
    
    insert_layout = dd.FormLayout("""
    question
    pub_date
    """,window_size=(40,'auto'))
    
    

class Choices(dd.Table):
    model = Choice
        
class ChoicesByPoll(Choices):
    master_key = 'poll'
    

def recent_polls(request):
    html = '<h1>%s</h1> ' % cgi.escape("Recent polls")
    html += '<ul>'
    for poll in Poll.objects.order_by('pub_date'):
        html += '<li>'
        html += '<b>%s</b> ' % cgi.escape(poll.question)
        chunks = []
        for obj in poll.choice_set.all():
            chunks.append(settings.LINO.ui.row_action_button(obj,request,Choices.vote,unicode(obj)))
        html += ' / '.join(chunks)
        
        html += "<br/><small>Published %s" % babel.dtosl(poll.pub_date)
        chunks = []
        for obj in poll.choice_set.all():
            chunks.append("%d %s" % (obj.votes,cgi.escape(unicode(obj))))
        html += '<br/>Results: %s' % (', '.join(chunks))
        html += '</small>'
        html += '</li>'
    html += '</ul>'
    return html
    
