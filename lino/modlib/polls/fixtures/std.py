# -*- coding: UTF-8 -*-
# Copyright 2013-2015 Luc Saffre
# License: BSD (see file COPYING for details)

from lino.api import dd, rt, _


def objects():

    polls = rt.modules.polls

    # yesno = polls.ChoiceSet(name="Yes/No")
    # yield yesno
    # yield polls.Choice(choiceset=yesno, name="Yes")
    # yield polls.Choice(choiceset=yesno, name="No")

    # maybe = polls.ChoiceSet(name=)
    # yield maybe
    # yield polls.Choice(choiceset=maybe, name="Yes")
    # yield polls.Choice(choiceset=maybe, name="Maybe")
    # yield polls.Choice(choiceset=maybe, name="No")

    def choiceset(name, *choices):
        namekw = dd.str2kw('name', name)
        cs = polls.ChoiceSet(**namekw)
        cs.save()
        for choice in choices:
            namekw = dd.str2kw('name', choice)
            obj = polls.Choice(choiceset=cs, **namekw)
            obj.full_clean()
            obj.save()
        return cs

    yesno = choiceset(_("Yes/No"), _("Yes"), _("No"))
    yield yesno
    maybe = choiceset(_("Yes/Maybe/No"), _("Yes"), _("Maybe"), _("No"))
    yield maybe
    yield choiceset(
        "That's it!...Never!", "That's it!", "Rather Yes",
        "Neutral", "Rather No", "Never!")
    yield choiceset("-1..+1", "-1", "0", "+1")

    yield choiceset(
        _("Acquired"), _("Acquired"), _("In progress"), _("Not acquired"))

    yield choiceset("1...5", "1", "2", "3", "4", "5")
    yield choiceset("1...10",
                    "1", "2", "3", "4", "5", "6", "7", "8", "9", "10")
