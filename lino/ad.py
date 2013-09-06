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
Example::

    from lino import ad
    
    class App(ad.App):
        extends = 'lino.modlib.cal'
        depends = ['lino.modlib.contacts']
    
"""
class App(object):
    """
    Don't instantiate, just subclass.
    """
    
    extends = None
    """
    The name of an app from which this app inherits.
    
    They must have the same "app_label"
    """
    
    verbose_name = None
    """
    TODO: if this is not None, then Lino will automatically 
    add a UserGroup.
    """
    
    depends = None
    """
    TODO: A list of names of apps that this app depends on.
    Lino will automatically add these to your 
    `INSTALLED_APPS` if necessary.
    Note that Lino will add them *after* your app.
    To have them *before* your app, specify them explicitly.
    
    """
    
    extends_models = None
    """
    If specified, a list of modlib model names for which this
    app provides a subclass.
    
    For backwards compatibility this has no effect
    when :attr:`lino.site.Site.override_modlib_models` is set.
    """
    
