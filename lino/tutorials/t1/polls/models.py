import cgi
import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings

from lino import dd
from lino.utils import babel


class Poll(dd.Model):
    question = models.CharField("Question text", max_length=200)
    hidden = models.BooleanField("Hidden",help_text="""\
Whether this poll should not be shown in the main window.""")
    pub_date = models.DateTimeField('Date published',auto_now_add=True)
    
    class Meta:
        verbose_name = 'Poll'
        verbose_name_plural = 'Polls'
    
    def __unicode__(self):
        return self.question
        
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - datetime.timedelta(days=1)        
        
class Choice(dd.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField("Choice text",max_length=200)
    votes = models.IntegerField("No. of votes",default=0)
    
    class Meta:
        verbose_name = 'Choice'
        verbose_name_plural = 'Choices'
    
    def __unicode__(self):
        return self.choice    

    @dd.action(help_text="Click here to see how Lino implements custom actions.")
    def vote(self,ar,**kw):
        if self.votes > 2:
            msg = "%s has already %d votes!" % (self,self.votes)
            msg += "\nDo you still want to vote for it?"
            ar.confirm(msg)
        self.votes += 1
        self.save()
        kw.update(refresh=True)
        kw.update(alert="Voted!")
        kw.update(message="Thank you for voting %s" % self)
        return ar.success_response(**kw)
        


class Polls(dd.Table):
    model = Poll
    sort_order = ['pub_date']
    
    detail_layout = """
    id question 
    hidden pub_date
    ChoicesByPoll
    """
    
    insert_layout = dd.FormLayout("""
    question
    hidden
    """,window_size=(40,'auto'))
    
    

class Choices(dd.Table):
    model = Choice
        
class ChoicesByPoll(Choices):
    master_key = 'poll'
    

def recent_polls(request):
    html = '<h1>%s</h1> ' % cgi.escape("Recent polls")
    html += '<ul>'
    for poll in Poll.objects.filter(hidden=False).order_by('pub_date'):
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
    
