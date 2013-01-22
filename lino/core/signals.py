## Copyright 2013 Luc Saffre
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

"""
This defines Lino's standard system signals.
"""

from django.dispatch import Signal

pre_analyze = Signal(['models_list'])
"""
Sent exactly once per process at site startup, just before Lino analyzes the models.

sender: 
  the Lino instance
  
models_list:
  list of models 
  
"""

post_analyze = Signal(['models_list'])
"""
Sent exactly once per process at site startup, 
just after Lino has finished to analyze the models.
"""

pre_startup = Signal(['model'])
"""
Sent exacty once per process before Lino starts up.
sender: 
  the Lino instance
"""



auto_create = Signal(["field","value"])
"""
The :attr:`auto_create` signal is sent when 
:func:`lookup_or_create` silently created a model instance.

Arguments sent with this signal:

``sender``
    The model instance that has been created. 
    
``field``
    The database field 

``known_values``
    The specified known values

"""
    

pre_merge = Signal(['merge_to'])
"""
Sent when a model instance is being merged into another instance.
"""

