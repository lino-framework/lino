## Copyright 2009-2010 Luc Saffre
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

import lino
from django.db import models
from django.db.models import loading

def welcome():

    for name,url,version in thanks_to():
        lino.log.info("%s %s <%s>",name,version,url)
    apps = app_labels()
      
    lino.log.debug("%d applications: %s.", len(apps),", ".join(apps))
    models_list = models.get_models()
    lino.log.debug("%d models:",len(models_list))
    i = 0
    for model in models_list:
        i += 1
        lino.log.debug("  %2d: %s.%s -> %r",i,model._meta.app_label,model._meta.object_name,model)
        #~ lino.log.debug("  %2d: %s %r",i,model._meta.db_table,model)
    
    
    
    
#~ def versions():
    #~ def HREF(name,url,version):
        #~ return mark_safe('<a href="%s">%s</a> %s' % (url,name,version))
    #~ for name,url,version in thanks_to():
        #~ yield HREF(name,url,version)
        
      
def thanks_to():
    yield ("Lino",
           "http://lino.saffre-rumma.ee",
           lino.__version__)
    
    import django
    yield ("Django",
           "http://www.djangoproject.com",
           django.get_version())
    
    import reportlab
    yield ("ReportLab Toolkit",
           "http://www.reportlab.org/rl_toolkit.html",
           reportlab.Version)
               
    import yaml
    version = getattr(yaml,'__version__','')
    yield ("PyYaml","http://pyyaml.org/",version)
    
    import dateutil
    version = getattr(dateutil,'__version__','')
    yield ("python-dateutil","http://labix.org/python-dateutil",version)
    
    import sys
    version = "%d.%d.%d" % sys.version_info[:3]
    yield ("Python","http://www.python.org/",version)
    
    try:
        # l:\snapshot\xhtml2pdf
        import ho.pisa as pisa
        version = getattr(pisa,'__version__','')
        yield ("xhtml2pdf","http://www.xhtml2pdf.com//",version)
    except ImportError:
        pisa = None
    

def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        
