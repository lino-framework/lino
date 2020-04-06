# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


from django.views.generic import View

from lino.core.requests import BaseRequest


class Element(View):

    publisher_model = None

    def get(self, request, pk=None):
        obj = self.publisher_model.objects.get(id=pk)
        ar = BaseRequest(request=request)
        return obj.get_publisher_response(ar)
