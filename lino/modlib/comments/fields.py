# -*- coding: UTF-8 -*-
# Copyright 2013-2020 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)

from lino.api import dd, rt

from .choicelists import Emotions

class MyEmotionField(dd.VirtualField):
    """
    An editable virtual field to get and set my emotion about that comment.

    My emotion is stored in the Emotion table.

    """

    editable = True
    empty_values = set([None])

    def __init__(self, *args, **kwargs):
        kwargs.update(blank=True)
        dd.VirtualField.__init__(self, Emotions.field(*args, **kwargs), None)
        self.choicelist = self.return_type.choicelist

    def set_value_in_object(self, ar, obj, value):
        if ar is None:
            raise Exception("20201215")
            # dd.logger.info("20201215 oops")
            # return
        mr, created = rt.models.comments.Reaction.objects.get_or_create(
            user=ar.get_user(), comment=obj)
        mr.emotion = value
        mr.full_clean()
        mr.save()

    def value_from_object(self, obj, ar=None):
        return obj.get_my_emotion(ar)
