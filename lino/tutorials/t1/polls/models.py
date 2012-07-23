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

    def summary_row(self,ar,**kw):
        html = '<b>%s</b> ' % cgi.escape(self.question)
        #~ raise Exception('20120723')
        #~ print ar
        chunks = []
        for obj in self.choice_set.all():
            #~ ar = self.request(ui,None,master_instance=master)
            chunks.append(ar.renderer.row_action_button(obj,ar,Choices.vote,unicode(obj)))
        html += ' / '.join(chunks)
        
        html += "<br/><small>Published %s" % babel.dtosl(self.pub_date)
        chunks = []
        for obj in self.choice_set.all():
            chunks.append("%d %s" % (obj.votes,cgi.escape(unicode(obj))))
        html += '<br/>Results: %s' % (', '.join(chunks))
        html += '</small>'
        return html


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
    
    
class PollsList(Polls):
    label = None
    slave_grid_format = 'summary'
    
      

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
        return ar.success_response(**kw)
        
    def __unicode__(self):
        return self.choice    
        
class Choices(dd.Table):
    model = Choice
        
class ChoicesByPoll(Choices):
    master_key = 'poll'
    

def site_setup(site):
    """
    (Called during site setup.)
    """
    site.modules.lino.Home.set_detail_layout("""
    polls.PollsList
    """)
    
    
    
