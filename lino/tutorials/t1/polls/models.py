import cgi
import datetime
from django.db import models
from django.conf import settings
from lino import dd
from lino.utils import babel

class Poll(models.Model):
    question = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published',auto_now_add=True)
    
    def __unicode__(self):
        return self.question
        
    def was_published_today(self):
        return self.pub_date.date() == datetime.date.today()        

    def summary_row(self,ui,**kw):
        html = '<b>%s</b> ' % cgi.escape(self.question)
        if True:
            html += ' / '.join([
                '<a href="oops">%s</a>' % cgi.escape(obj.choice)
                    for obj in self.choice_set.all()])
        else:
            chunks = []
            for obj in self.choice_set.all():
                ar = Choices.row_action_request('vote',choice)
                chunks.append(ui.ext_renderer.href_to_request(ar))
                #~ html += ui.ext_renderer.href_to(VoteAction(choice))
            html += ' / '.join(chunks)
        html += "<br/><small>(published %s)</small>" % babel.dtosl(self.pub_date)
        return html
      
      
class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)
    
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
    
    
from lino import models as lino

class Home(lino.Home):
    detail_template = """
    welcome
    """
    @dd.displayfield()
    def welcome(cls,self,ar):
        s = "<p>Welcome to the <b>%s</b> server.</p>" % cgi.escape(settings.LINO.title)
        s += dd.summary(ar.ui,Poll.objects.all(),
          separator='</li><li>',before="<ul><li>",after="</li></ul>")
        return '<div class="htmlText">%s</div>' % s

    
    
#~ def summary(ui,objects,separator=', ',max_items=5,before='',after='',**kw):
    