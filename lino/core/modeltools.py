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

"""modeltools may not be used in models modules (but well during lino_site set up).
"""

import logging
logger = logging.getLogger(__name__)


import os
import sys

from django.db import models
from django.conf import settings
from django.db.models import Q
from django.db.models.fields import FieldDoesNotExist
from django.utils.importlib import import_module
from django.db.models import loading
#~ from lino.core import actors
from lino.utils import get_class_attr


from django.core.validators import validate_email, ValidationError, URLValidator
validate_url = URLValidator()
def is_valid_url(s):
    try:
        validate_url(s)
        return True
    except ValidationError:
        return False
        
def is_valid_email(s):
    try:
        validate_email(s)
        return True
    except ValidationError:
        return False
        
        
class Model(models.Model):
    """
    Adds Lino specific features to Django's Model base class. 
    If a Lino application uses simple Django Models,
    the attributes and methods defined here are added to these 
    modules during :func:`lino.core.kernel.analyze_models`.
    """
    class Meta:
        abstract = True
        
    allow_cascaded_delete = False
    """
    Lino, like Django, by default forbids to delete an object that is 
    referenced by other objects.

    Set this to `True` on models whose objects should get automatically 
    deleted if a related object gets deleted. 
    Example: Lino should not refuse to delete 
    a Mail just because it has some Recipient. 
    When deleting a Mail, Lino should also delete its Recipients.
    That's why :class:`lino.modlib.outbox.models.Recipient` 
    has ``allow_cascaded_delete = True``.
    
    Other examples of such models are 
    :class:`lino.modlib.cv.models.PersonProperty`,
    :class:`lino.modlib.cv.models.LanguageKnowledge`,
    :class:`lino.modlib.debts.models.Actor`,
    :class:`lino.modlib.debts.models.Entry`,
    ...
    
    Not that this currently is also consulted by
    :meth:`lino.mixins.duplicable.Duplicable.duplicate_row`
    to decide whether slaves of a record being duplicated
    should be duplicated as well.
    
    """
    
    quick_search_fields = None
    """
    When quick_search text is given for a table on this model, 
    Lino by default searches the query text in all CharFields.
    But on models with `quick_search_fields` will search only those fields.
    
    This is also used when a gridfilter has been set on a 
    foreign key column which points to this model. 
    
    """
    
    #~ grid_search_field = None
    #~ """
    #~ The name of the field to be used when a gridfilter has been set on a 
    #~ foreign key column which points to this model. Capito?
    #~ """

    
    workflow_state_field = None
    """
    If this is set on a Model, then it will be used as default 
    value for :attr:`lino.core.table.Table.workflow_state_field` 
    on all tables based on this Model.
    """
    
    workflow_owner_field = None
    """
    If this is set on a Model, then it will be used as default 
    value for :attr:`lino.core.table.Table.workflow_owner_field` 
    on all tables based on this Model.
    """
    
    def disable_delete(self):
        """
        Return None if it is okay to delete this object,
        otherwise a nonempty string explaining why.
        """
        return self._lino_ddh.disable_delete_on_object(self)
        
    def disabled_fields(self,ar):
        return []
        
    def on_create(self,ar):
        """
        Used e.g. by modlib.notes.Note.on_create().
        on_create gets the action request as argument.
        Didn't yet find out how to do that using a standard Django signal.
        """
        pass
        
    def before_ui_save(self,ar):
        """
        Called after a PUT or POST on this row, and before saving the row.
        Example in :class:`lino.modlib.cal.models.Event` to mark the 
        event as user modified by setting a default state.
        """
        pass
        
    def after_ui_save(self,ar,**kw):
        """
        Called after a PUT or POST on this row, 
        and after the row has been saved.
        It must return (and may modify) the `kw` which will become 
        the ajax response to the save() call.
        Used by :class:`lino.modlib.debts.models.Budget` 
        to fill default entries to a new Budget,
        or by :class:`lino.modlib.cbss.models.CBSSRequest` 
        to execute the request.
        """
        return kw
        
    def get_row_permission(self,user,state,action):
        """
        Returns True or False whether this row instance 
        gives permission the specified user to run the specified action.
        """
        return action.get_action_permission(user,self,state)

    def update_owned_instance(self,controllable):
        """
        Called by :class:`lino.mixins.Controllable`.
        """
        #~ print '20120627 tools.Model.update_owned_instance'
        pass
                
    def after_update_owned_instance(self,controllable):
        """
        Called by :class:`lino.mixins.Controllable`.
        """
        pass
        
    def get_mailable_recipients(self):
        """
        Return or yield a list of (type,partner) tuples to be 
        used as recipents when creating an outbox.Mail from this object.
        """
        return []
        
    def get_postable_recipients(self):
        """
        Return or yield a list of Partners to be 
        used as recipents when creating a posting.Post from this object.
        """
        return []
        
    @classmethod
    def site_setup(self,site):
        pass
        
    @classmethod
    def setup_table(cls,t):
        """
        Called during site startup once on each Table that 
        uses this model.
        """
        pass
        
    def on_duplicate(self,ar,master):
        """
        Called by :meth:`lino.mixins.duplicable.Duplicable.duplicate_row`.
        `ar` is the action request that asked to duplicate.
        If `master` is not None, then this is a cascaded duplicate initiated
        be a duplicate() on the specifie `master`.
        """
        pass
        
    def before_state_change(self,ar,kw,old,new):
        """
        Called before a state change.
        """
        pass
  
    def after_state_change(self,ar,kw,old,new):
        """
        Called after a state change.
        """
        kw.update(refresh=True)
        
    def after_send_mail(self,mail,ar,kw):
        """
        Called when an outbox email controlled by self has been sent
        (i.e. when the :class:`lino.modlib.outbox.models.SendMail` 
        action has successfully completed).
        """
        pass
  
    def summary_row(self,ar,**kw):
        return ar.href_to(self)
        
def is_devserver():
    """
    Returns True if we are running a development server.
    
    Thanks to Aryeh Leib Taurog in 
    `How can I tell whether my Django application is running on development server or not?
    <http://stackoverflow.com/questions/1291755>`_
    
    Added the `len(sys.argv) > 1` test because in a 
    wsgi application the process is called without arguments.
    """
    return len(sys.argv) > 1 and sys.argv[1] == 'runserver'


def resolve_app(app_label):
    """
    Return the `modules` module of the given `app_label` if it is installed, 
    otherwise `None`.
    
    This is called in models modules instead of "from x.y import models as y"
    May not be called during loading.appcache._populate().
    
    It is probably quicker than `django.db.loading.get_app()`.
    Didn't test how they compare in multi-threading cases.
    
    """
    for app_name in settings.INSTALLED_APPS:
        if app_name.endswith('.'+app_label):
            return import_module('.models', app_name)
    #~ if not emptyOK:
    #~ raise ImportError("No application labeled %r." % app_label)
#~ resolve_app = get_app

#~ def get_models_for(app_label):
    #~ a = models.get_app(app_label)
    
class UnresolvedModel:
    """
    This is the object returned by :func:`resolve_model` 
    if the specified model is not installed.
    
    We don't want resolve_model to raise an Exception because there are 
    cases of :doc:`data migration </topics/datamig>` where it would 
    disturb. 
    Asking for a non-installed model is not a sin, but trying to use it is.
    
    I didn't yet bother very much about finding a way to make the 
    model_spec appear in error messages such as
    ``AttributeError: UnresolvedModel instance has no attribute '_meta'``.
    Current workaround is to uncomment the ``print`` statement 
    below in such situations...
    
    """
    def __init__(self,model_spec,app_label):
        self.model_spec = model_spec
        self.app_label = app_label
        #~ print repr(self)
        
    def __repr__(self):
        return self.__class__.__name__ + '(%s,%s)' % (self.model_spec,self.app_label)
        
    #~ def __getattr__(self,name):
        #~ raise AttributeError("%s has no attribute %r" % (self,name))

def resolve_model(model_spec,app_label=None,strict=False,seed_cache=True):
    """
    See also django.db.models.fields.related.add_lazy_relation()
    """
    #~ models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
            
        #~ try:
            #~ app_label, model_name = model_spec.split(".")
        #~ except ValueError:
            #~ # If we can't split, assume a model in current app
            #~ #app_label = rpt.app_label
            #~ model_name = model_spec
            
        #~ model = models.get_model(app_label,model_name,seed_cache=False)
        model = models.get_model(app_label,model_name,seed_cache=seed_cache)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            raise Exception(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                model_spec,app_label,model,settings.SETTINGS_MODULE))
        #~ logger.info("20120628 unresolved %r",model)
        return UnresolvedModel(model_spec,app_label)
    return model
    
def old_resolve_model(model_spec,app_label=None,strict=False):
    """
    doesn't work for contacts.Company because the model is defined somewhere else.
    """
    models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec,basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec
        app = resolve_app(app_label)
        model = getattr(app,model_name,None)
    else:
        model = model_spec
    if not isinstance(model,type) or not issubclass(model,models.Model):
        if strict:
            raise Exception(
                "resolve_model(%r,app_label=%r) found %r (settings %s)" % (
                model_spec,app_label,model,settings.SETTINGS_MODULE))
        return UnresolvedModel(model_spec,app_label)
    return model
    
def get_field(model,name):
    '''Returns the field descriptor of the named field in the specified model.
    '''
    for vf in model._meta.virtual_fields:
        if vf.name == name:
            return vf
    fld, remote_model, direct, m2m = model._meta.get_field_by_name(name)
    # see blog/2011/0525
    #~ if remote_model is not None:
        #~ raise Exception("get_field(%r,%r) got a remote model ?!" % (model,name))
    return fld
  
class UnresolvedField(object):
    """
    Returned by :func:`resolve_field` if the specified field doesn't exist.
    This case happens when sphinx autodoc tries to import a module.
    See ticket :doc:`/tickets/4`.
    """
    def __init__(self,name):
        self.name = name
        self.verbose_name = "Unresolved Field " + name

def resolve_field(name,app_label=None):
    """
    Returns the field descriptor specified by the string `name` which 
    should be either `model.field` or `app_label.model.field`.
    """
    l = name.split('.')
    if len(l) == 3:
        app_label = l[0]
        del l[0]
    if len(l) == 2:
        #print "models.get_model(",app_label,l[0],False,")"
        model = models.get_model(app_label,l[0],False)
        if model is not None:
            try:
                fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
            except FieldDoesNotExist:
                return UnresolvedField(name)
            assert remote_model is None or issubclass(model,remote_model), \
                "resolve_field(%r) : remote model is %r (expected None or base of %r)" % (name,remote_model,model)
            return fld
    return UnresolvedField(name)


#~ def requires_apps(self,*app_labels):
    #~ for app_label in app_labels:
        #~ get_app(app_label)
    
    
    
def full_model_name(model,sep='.'):
    """Returns the "full name" of the given model, e.g. "contacts.Person" etc.
    """
    return model._meta.app_label + sep + model._meta.object_name
    
    
    
def obj2unicode(i):
    """Returns a user-friendly unicode representation of a model instance."""
    return u'%s "%s"' % (i._meta.verbose_name,unicode(i))
    
def obj2str(i,force_detailed=False):
    """
    Returns a usable ascii string representation of a model instance, 
    even in some edge cases.
    """
    #~ if not force_detailed and i.pk is not None:
    if not isinstance(i,models.Model): 
        if isinstance(i,long): return str(i) # AutoField is long on mysql, int on sqlite
        return repr(i)
    if i.pk is None:
        force_detailed = True
    if not force_detailed:
        if i.pk is None:
            return '(Unsaved %s instance)' % (i.__class__.__name__)
        try:
            return u"%s #%s (%s)" % (i.__class__.__name__,str(i.pk),repr(unicode(i)))
        except Exception,e:
        #~ except TypeError,e:
            return "Unprintable %s(pk=%r,error=%r" % (
              i.__class__.__name__,i.pk,e)
            #~ return unicode(e)
    #~ names = [fld.name for (fld,model) in i._meta.get_fields_with_model()]
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in names])
    pairs = []
    for (fld,model) in i._meta.get_fields_with_model():
        if isinstance(fld,models.ForeignKey):
            v = getattr(i,fld.attname) 
            #~ v = getattr(i,fld.name+"_id") 
            #~ if getattr(i,fld.name+"_id") is not None:
                #~ v = getattr(i,fld.name)
        else:
            v = getattr(i,fld.name)
        if v:
            pairs.append("%s=%s" % (fld.name,obj2str(v)))
    s = ','.join(pairs)
    #~ s = ','.join(["%s=%s" % (n, obj2str(getattr(i,n))) for n in names])
    #~ print i, i._meta.get_all_field_names()
    #~ s = ','.join(["%s=%r" % (n, getattr(i,n)) for n in i._meta.get_all_field_names()])
    return "%s(%s)" % (i.__class__.__name__,s)


def sorted_models_list():
    models_list = models.get_models() # trigger django.db.models.loading.cache._populate()
    def fn(a,b):
        return cmp(full_model_name(a),full_model_name(b))
    models_list.sort(fn)
    return models_list

def models_by_abc(abc):
    """
    Yields a list of installed models that are 
    subclass of the given abstract base class.
    """
    for m in models.get_models():
        if issubclass(m,abc):
            yield m
    

def makedirs_if_missing(dirname):
    """
    Make missing directories if they don't exist 
    and if :attr:`lino.Lino.make_missing_dirs` 
    is `True`.
    """
    #~ if not os.path.exists(dirname):
        #~ os.makedirs(dirname)
    if not os.path.isdir(dirname):
        if settings.LINO.make_missing_dirs:
            os.makedirs(dirname)
        else:
            raise Exception("Please create yourself directory %s" % dirname)
        
def range_filter(v,f1,f2):
    """
    Returns a Q object (to be added as a filter on a queryset)
    to inlude only instances where v is contained within the range between f1 and f2.
    `v` being a value and f1 and f2 being the names of fields of same data type as v.
    """
    #~ filter = Q(**{f2+'__isnull':False}) | Q(**{f1+'__isnull':False})
    q1 = Q(**{f1+'__isnull':True}) | Q(**{f1+'__lte':v})
    q2 = Q(**{f2+'__isnull':True}) | Q(**{f2+'__gte':v})
    return Q(q1,q2)
  




def app_labels():
    return [a.__name__.split('.')[-2] for a in loading.get_apps()]
        
#~ def get_slave(model,name):
    #~ """Return the named table, knowing that it is a 
    #~ slave of the specified `model`. 
    #~ If name has no app_label specified, use the model's app_label.
    #~ """
    #~ if not '.' in name:
        #~ name = model._meta.app_label + '.' + name
    #~ rpt = actors.get_actor(name)
    #~ if rpt is None: 
        #~ return None
    #~ return rpt

def get_model_report(model):
    if not hasattr(model,'_lino_default_table'):
        raise Exception("%r has no _lino_default_table" % model)
    return model._lino_default_table

def get_unbound_meth(cl,name):
    raise Exception("replaced by lino.utils.get_class_attr")
    
    
def get_data_elem(model,name):
    #~ logger.info("20120202 get_data_elem %r,%r",model,name)
    try:
        return model._meta.get_field(name)
    except models.FieldDoesNotExist,e:
        pass
        
    #~ s = name.split('.')
    #~ if len(s) == 1:
        #~ mod = import_module(model.__module__)
        #~ rpt = getattr(mod,name,None)
    #~ elif len(s) == 2:
        #~ mod = getattr(settings.LINO.modules,s[0])
        #~ rpt = getattr(mod,s[1],None)
    #~ else:
        #~ raise Exception("Invalid data element name %r" % name)
    
    v = get_class_attr(model,name)
    if v is not None: return v
    
    for vf in model._meta.virtual_fields:
        if vf.name == name:
            return vf

