import cgi
import datetime
from django.utils import timezone
from django.db import models
from django.conf import settings

from lino import dd


class Poll(dd.Model):
    question = models.CharField("Question text", max_length=200)
    hidden = models.BooleanField("Hidden",help_text="""\
Whether this poll should not be shown in the main window.""",default=False)
    #~ pub_date = models.DateTimeField('Date published',auto_now_add=True)
    pub_date = models.DateTimeField('Date published',default=datetime.date.today)
    
    input_mask_test = dd.CharField("Question text", 
        blank=True,
        max_length=200,
        help_text="""This field is here to play with the 
        CharField parameters regex, mask_re and strip_chars_re.
        By default it accepts all letters except Z.
        """,
        #~ regex='/^[a-yA-Y]*$/')
        mask_re='/^[a-yA-Y]*$/')
        #~ strip_chars_re='/^[a-yA-Y]*$/')
    
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

    @dd.action(help_text="Click here to vote this.")
    def vote(self,ar):
        def yes(ar):
            self.votes += 1
            self.save()
            return ar.success(
                "Thank you for voting %s" % self,
                "Voted!",refresh=True)
        if self.votes > 0:
            msg = "%s has already %d votes!" % (self,self.votes)
            msg += "\nDo you still want to vote for it?"
            return ar.confirm(yes,msg)
        return yes(ar)
        


class Polls(dd.Table):
    model = Poll
    sort_order = ['pub_date']
    
    detail_layout = """
    id question 
    hidden pub_date input_mask_test
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


def setup_main_menu(site,ui,profile,main):
    m = main.add_menu("polls","~Polls")
    m.add_action(site.modules.polls.Polls)
    m.add_action(site.modules.polls.Choices)
