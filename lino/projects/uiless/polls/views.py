from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.http import Http404
from django.template import Context, loader

from polls.models import Poll

#~ def index(request):
    #~ return HttpResponse("Hello, world. You're at the poll index.")
    
#~ def index(request):
    #~ latest_poll_list = Poll.objects.order_by('-pub_date')[:5]
    #~ context = Context({
        #~ 'latest_poll_list': latest_poll_list,
    #~ })
    #~ return render(request, 'polls/index.html', context)
    
#~ def detail(request, poll_id):
    #~ return HttpResponse("You're looking at poll %s." % poll_id)

#~ def detail(request, poll_id):
    #~ poll = get_object_or_404(Poll, pk=poll_id)
    #~ try:
        #~ poll = Poll.objects.get(pk=poll_id)
    #~ except Poll.DoesNotExist:
        #~ raise Http404
    #~ return render(request, 'polls/detail.html', {'poll': poll})    
    
#~ def results(request, poll_id):
    #~ return HttpResponse("You're looking at the results of poll %s." % poll_id)
    
#~ def results(request, poll_id):
    #~ poll = get_object_or_404(Poll, pk=poll_id)
    #~ return render(request, 'polls/results.html', {'poll': poll})    

#~ def vote(request, poll_id):
    #~ return HttpResponse("You're voting on poll %s." % poll_id)    
    
    
    
    
#~ from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from polls.models import Choice, Poll
# ...
def vote(request, poll_id):
    p = get_object_or_404(Poll, pk=poll_id)
    try:
        selected_choice = p.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        # Redisplay the poll voting form.
        return render(request, 'polls/detail.html', {
            'poll': p,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        # Always return an HttpResponseRedirect after successfully dealing
        # with POST data. This prevents data from being posted twice if a
        # user hits the Back button.
        return HttpResponseRedirect(reverse('polls:results', args=(p.id,)))    
        