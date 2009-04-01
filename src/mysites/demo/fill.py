## Copyright 2008-2009 Luc Saffre 

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
import settings
from django.core.management import setup_environ
setup_environ(settings)
from django.contrib.auth.models import User
from django.core.management.color import no_style
from django.db import models, connection, transaction, models
from django.core.management.sql import sql_flush, emit_post_sync_signal
from django.core.management import call_command



from lino.tools.yamlloader import YamlLoader


class Converter:
    def __init__(self,field):
        self.field = field
  
    def convert(self,**kw):
        return kw
      
class ForeignKeyConverter(Converter):
    def convert(self,**kw):
        pkvalue = kw.get(self.field.name)
        if pkvalue is not None:
            kw[self.field.name] = self.field.rel.to.objects.get(pk=pkvalue)
        return kw
    
      
class ModelBuilder:
    def __init__(self,model_class):
        self.model_class = model_class
        self.converters = []
        #print " ".join(dir(model_class))
        #print " ".join(model_class._meta.fields)
        for f in model_class._meta.fields:
            #f = getattr(model_class,name)
            #print repr(f)
            if isinstance(f,models.ForeignKey):
                self.converters.append(ForeignKeyConverter(f))
            
    def build(self,**kw):
        print "build",kw
        for c in self.converters:
            kw = c.convert(**kw)
        return self.model_class(**kw)
  

class Filler(YamlLoader):
  
    usage="""

Deletes all content nodes from the database and fills it with data from input files.

How to use this script:

<pre>
python fill.py demo.yaml
</pre>

"""
    input_dirs = ["data"]
    model_builder = None
    
    def add_from_file(self,filename,full_path,values):
        if values.has_key('model'):
            modelspec = values.pop('model')
            #model_class = eval(modelspec)
            app,model=modelspec.split(".")
            #print app,model
            model_class = models.get_model(app,model)
            self.model_builder = ModelBuilder(model_class)
        if self.model_builder is None:
            raise Exception("no model specified")
        #print model_class
        instance = self.model_builder.build(**values)
        #~ if model_class == User:
            #~ instance.set_password(yamldict.get('password'))
        # data files are required to use "!!python/object:", so the
        # yamldict is a Python object
        #self.add_node(yamldict)
        instance.save()
        print "Saved:", instance
        #self.modelspec = modelspec
        
        
    def run(self):
        if self.confirm("Gonna flush database %s. Are you sure?" 
            % settings.DATABASE_NAME):
            call_command('flush')
        elif not self.confirm("Continue filling the existing database?"):
            return
        #call_command('syncdb')
        User.objects.create_superuser('root','root@example.com','root')
        User.objects.create_user('user','user@example.com','user')
        YamlLoader.run(self)
        

if __name__ == "__main__":
    Filler().main()
