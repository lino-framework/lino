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
        if False:
            html += ' / '.join([
                '<a href="oops">%s</a>' % cgi.escape(obj.choice)
                    for obj in self.choice_set.all()])
        else:
            """
            TODO: change summary_row() signature to include `ar`
            """
            chunks = []
            for obj in self.choice_set.all():
                #~ ar = self.request(ui,None,master_instance=master)
                chunks.append(ar.renderer.row_action_button(obj,ar,ar.actor.vote))
                #~ ar = Choices.row_action_request('vote',choice)
                #~ chunks.append(ui.ext_renderer.href_to_request(ar))
            html += ' / '.join(chunks)
        html += "<br/><small>(published %s)</small>" % babel.dtosl(self.pub_date)
        return html
      
      
class Choice(dd.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
    @dd.action()
    def vote(self,ar,**kw):
        self.votes += 1
        self.save()
        
    def __unicode__(self):
        return self.choice    
        


class Polls(dd.Table):
    debug_permissions = True
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
    
    
class PollsList(Polls):
    label = None
    slave_grid_format = 'summary'
    

def site_setup(site):
    """
    (Called during site setup.)
    """
    site.modules.lino.Home.set_detail_layout("""
    polls.PollsList
    """)
    
    
    
#~ from lino import models as lino

#~ class Home(lino.Home):
    #~ app_label = 'lino'
    #~ detail_template = """
    #~ welcome
    #~ """
    #~ @dd.displayfield()
    #~ def welcome(cls,self,ar):
        #~ s = "<p>Welcome to the <b>%s</b> server.</p>" % cgi.escape(settings.LINO.title)
        #~ s += dd.summary(ar.ui,Poll.objects.all(),
          #~ separator='</li><li>',before="<ul><li>",after="</li></ul>")
        #~ return '<div class="htmlText">%s</div>' % s

    
    
    