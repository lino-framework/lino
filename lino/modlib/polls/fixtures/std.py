# -*- coding: UTF-8 -*-
# Copyright 2013-2014 Luc Saffre
# License: BSD (see file COPYING for details)

from lino import rt
from lino.ad import _


def objects():

    polls = rt.modules.polls

    yesno = polls.ChoiceSet(name="Yes/No")
    yield yesno
    yield polls.Choice(choiceset=yesno, name="Yes")
    yield polls.Choice(choiceset=yesno, name="No")

    maybe = polls.ChoiceSet(name="Yes/Maybe/No")
    yield maybe
    yield polls.Choice(choiceset=maybe, name="Yes")
    yield polls.Choice(choiceset=maybe, name="Maybe")
    yield polls.Choice(choiceset=maybe, name="No")

    def choiceset(name, *choices):
        cs = polls.ChoiceSet(name=name)
        cs.save()
        for choice in choices:
            obj = polls.Choice(choiceset=cs, name=choice)
            obj.full_clean()
            obj.save()
        return cs

    yield choiceset(
        "Rather Yes/No", "That's it!", "Rather Yes",
        "Neutral", "Rather No", "Never!")
    yield choiceset("-1..+1", "-1", "0", "+1")

    yield choiceset(
        _("Acquired"), _("Acquired"), _("In progress"), _("Not acquired"))
