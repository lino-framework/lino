# -*- coding: UTF-8 -*-
# Copyright 2020 Rumma & Ko Ltd
# License: BSD (see file COPYING for details)


import logging ; logger = logging.getLogger(__name__)

from django.views.generic import View





class Element(View):
    
    publisher_model = None

    def get(self, request, pk=None):
        obj = self.publisher_model.objects.get(id=pk)
        return obj.get_publisher_response(request)
