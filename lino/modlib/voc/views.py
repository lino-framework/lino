## Copyright 2008-2010 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

from django.shortcuts import render_to_response
from django.shortcuts import get_object_or_404
#from django.http import HttpResponse
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from lino.modlib.voc import models


def unit_list(request):
    """
    """
    return render_to_response("voc/unit_list.html", 
         dict(units=models.Unit.objects.all()))
      
#~ def course_list(request):
    #~ """
    #~ """
    #~ return render_to_response("voc/course_list.html", 
         #~ dict(courses=models.Course.objects.all()))
      
def unit_detail(request, unit_id):
    """
    """
    unit = get_object_or_404(models.Unit,pk=unit_id)
    #~ try:
        #~ unit = models.Unit.get(pk=unit_id)
    #~ except ObjectDoesNotExist:
        #~ raise Http404, "%s : no such unit" % (pk)
    
    return render_to_response("voc/unit_detail.html", 
          dict(unit=unit))
      
#~ def course_detail(request, course_id):
    #~ """
    #~ """
    #~ course = get_object_or_404(models.Course,pk=course_id)
    #~ return render_to_response("voc/course_detail.html", 
          #~ dict(course=course))
      

      
def entry_page(request, unit_id, page):
    """
    """
    unit = get_object_or_404(models.Unit,pk=unit_id)
    paginator = Paginator(unit.entry_set.all(), 1) # 1 Entry per page
    #~ if not page:
        #~ page = request.GET.get('page', "1")
    #~ try:
        #~ page = int(page)
    #~ except ValueError:
        #~ page=1
    try:
        page_obj = paginator.page(page)
    except (EmptyPage, InvalidPage):
        page_obj = paginator.page(paginator.num_pages)
    #assert len(page_object.object_list) == 1
    entry=page_obj.object_list[0]
    return render_to_response('voc/entry_page.html', 
      dict(entry=entry, page_obj=page_obj))

      

def entry_detail(request, pk):
    """
    """
    obj = get_object_or_404(models.Entry,pk=pk)
    #~ try:
        #~ obj = models.Entry.get(pk=pk)
    #~ except ObjectDoesNotExist:
        #~ raise Http404, "%s : no such entry" % (pk)
    
    return render_to_response("voc/entry_detail.html", 
          dict(entry=obj))
