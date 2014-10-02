# -*- coding: UTF-8 -*-
# Copyright 2014 Luc Saffre
# License: BSD (see file COPYING for details)

from django.conf import settings
from lino import rt
from lino.utils import Cycler


def objects():

    polls = rt.modules.polls

    five = polls.ChoiceSet.objects.get(name="1...5")
    ten = polls.ChoiceSet.objects.get(name="1...10")

    USERS = Cycler(settings.SITE.user_model.objects.all())

    def poll(choiceset, title, details, questions):
        return polls.Poll(
            user=USERS.pop(),
            title=title.strip(),
            details=details.strip(),
            state=polls.PollStates.published,
            questions_to_add=questions,
            default_choiceset=choiceset)

    yield poll(ten, "Customer Satisfaction Survey", """
Please give your vote for each aspect of our company.
""", """
%(X)s has a good quality/price ratio.
%(X)s is better than their concurrents.
%(X)s has an attractive website.
%(X)s values my money.
I am proud to be a customer of %(X)s.
I would recommend %(X)s to others.
""" % dict(X="Polls Mentor Ltd."))

    yield poll(five, "Participant feedback", """
Please give your vote for each aspect of the event.
""", """
There was enough to eat.
The stewards were nice and attentive.
The participation fee was worth the money.
Next time I will participate again.
""" % dict(X="Lino Polly"))

    for p in polls.Poll.objects.exclude(questions_to_add=''):
        p.after_ui_save(None)
        #~ p.save()
        yield polls.Response(poll=p, user=USERS.pop())
