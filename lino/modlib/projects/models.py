# -*- coding: UTF-8 -*-
## Copyright 2009-2012 Luc Saffre
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

u"""
Projects
--------

Adds tables Project and ProjectType

"""

from django.db import models
from django.utils.translation import ugettext as _

from lino import dd
from lino import mixins
from lino.utils import babel


class ProjectType(babel.BabelNamed):
    class Meta:
        verbose_name = _("Project Type")
        verbose_name_plural = _("Project Types")
        

class ProjectTypes(dd.Table):
    model = ProjectType
    order_by = ["name"]

#
# PROJECT
#
class Project(mixins.AutoUser,mixins.CachedPrintable):
  
    class Meta:
        verbose_name = _("Project")
        verbose_name_plural = _("Projects")
        
    name = models.CharField(max_length=200)
    type = models.ForeignKey(ProjectType,blank=True,null=True)
    started = models.DateField(blank=True,null=True) 
    stopped = models.DateField(blank=True,null=True) 
    text = models.TextField(blank=True,null=True)
    
    def __unicode__(self):
        return self.name
        
#~ class ProjectDetail(layouts.DetailLayout):
    #~ datalink = 'projects.Project'
    #~ main = """
    #~ name type
    #~ started stopped
    #~ text
    #~ """

class Projects(dd.Table):
    model = 'projects.Project'
    order_by = ["name"]
    button_label = _("Projects")
    detail_template = """
    name type user
    started stopped
    text
    """
    
class MyProjects(Projects,mixins.ByUser):
    pass
    

MODULE_NAME = _("Projects")

def site_setup(site):  pass

def setup_main_menu(site,ui,user,m):  pass
  
def setup_master_menu(site,ui,user,m): pass

def setup_my_menu(site,ui,user,m): 
    m  = m.add_menu("debts",MODULE_NAME)
    m.add_action(MyProjects)
  
def setup_config_menu(site,ui,user,m): 
    m  = m.add_menu("debts",MODULE_NAME)
    #~ m.add_action(Accounts)
    m.add_action(ProjectTypes)
  
def setup_explorer_menu(site,ui,user,m):
    m  = m.add_menu("debts",MODULE_NAME)
    m.add_action(Projects)
