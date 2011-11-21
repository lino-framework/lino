from lino.django.polls.models import Poll, Choice
from lino.django.nodes.models import Node
from django.contrib import admin
from django.contrib import databrowse


class ChoiceInline(admin.TabularInline):
#class ChoiceInline(admin.StackedInline):
    model = Choice
    extra = 3

class PollAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               dict(fields=['question'])),
        ('Date information', dict(fields=['pub_date'], 
          classes=['collapse'])),
    ]
    inlines = [ChoiceInline]
    list_display = ('question', 'pub_date', 'was_published_today')
    list_filter = ['pub_date']
    search_fields = ['question']
    date_hierarchy = 'pub_date'
    
    

admin.site.register(Poll, PollAdmin)

databrowse.site.register(Node)
databrowse.site.register(Poll)
databrowse.site.register(Choice)
