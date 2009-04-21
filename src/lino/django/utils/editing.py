## Copyright 2009 Luc Saffre

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

import os

"""
This middleware manages the "editing" status of a Session. 

Views should not pay attention (nor modify) the "editing" key in request.GET and in request.session.
Views are supposed to call is_editing() to determine whether they should
render an editable version or not.

Internally, editing is activated by a GET editing=1, 
stopped explicitly by GET editing=0, or stopped automatically 
if the request.path changes. Editing is also "sticky", if theres no
"editing" key requested, then the previous request's value is 
maintained.


There can be more than one renderers in a single request. 
When a renderer says stop_editing(), then this should become 
active only for the next request, other renderers of the same 
request must still get True when they call is_editing().

If a renderer calls stop_editing() and some other renderer 
(before or after) calls continue_editing(), then editing continues.

Example: when a renderer saves successfully, then it calls stop_editing(). But if some other renderer detects a validation error, then it calls continue_editing() and this will override the stop call of the first renderer.

"""


class EditingMiddleware:
    def process_request(self, request):
        request.stop_editing = False
        request.continue_editing = False
        editing = request.GET.get("editing",None)
        if editing is not None:
            editing = int(editing)
            if editing:
                request.session["editing"] = path = request.path
            else:
                request.session["editing"] = path = None
        
    def process_response(self, request, response):
        if request.stop_editing and not request.continue_editing:
            request.session["editing"] = None
        return response
            

def is_editing(request):
    path = request.session.get("editing",None)
    return request.path == path

def stop_editing(request):
    request.stop_editing = True
    #request.session["editing"] = None

def continue_editing(request):
    request.continue_editing = True
    
#~ def start_editing(request):
    #~ request.session["editing"] = request.path
    
