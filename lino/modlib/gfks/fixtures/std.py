# -*- coding: UTF-8 -*-
# Copyright 2011-2015 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.utils.instantiator import Instantiator

from lino.api import rt


def objects():
    HelpText = rt.models.gfks.HelpText
    ContentType = rt.models.contenttypes.ContentType
    HT = Instantiator(HelpText, "content_type field help_text").build
    yield HT(ContentType.objects.get_for_model(HelpText),
             'field', "The name of the field.")
