# -*- coding: UTF-8 -*-
# Copyright 2009-2014 Luc Saffre
# License: BSD (see file COPYING for details)

"""
A collection of database utilities, i.e. Django-related

"""

from __future__ import unicode_literals


import logging
logger = logging.getLogger(__name__)

from django.db import models
from django.conf import settings
from django.db.models.fields import FieldDoesNotExist
from django.utils.importlib import import_module
from django.utils.translation import ugettext as _

from djangosite.dbutils import obj2str, full_model_name, app_labels
from djangosite.dbutils import sorted_models_list
from djangosite.dbutils import is_devserver
from djangosite.dbutils import is_valid_email
from djangosite.dbutils import is_valid_url
from djangosite import AFTER17


def babelkw(*args, **kw):
    return settings.SITE.babelkw(*args, **kw)


def babelattr(*args, **kw):
    return settings.SITE.babelattr(*args, **kw)
babel_values = babelkw  # old alias for backwards compatibility


class UnresolvedModel:

    """
    This is the object returned by :func:`resolve_model` 
    if the specified model is not installed.
    
    We don't want resolve_model to raise an Exception because there are 
    cases of :ref:`datamig` where it would disturb. 
    Asking for a non-installed model is not a sin, but trying to use it is.
    
    I didn't yet bother very much about finding a way to make the 
    model_spec appear in error messages such as
    ``AttributeError: UnresolvedModel instance has no attribute '_meta'``.
    Current workaround is to uncomment the ``print`` statement 
    below in such situations...
    
    """

    def __init__(self, model_spec, app_label):
        self.model_spec = model_spec
        self.app_label = app_label
        #~ print(self)

    def __repr__(self):
        return self.__class__.__name__ + '(%s,%s)' % (
            self.model_spec, self.app_label)

    #~ def __getattr__(self,name):
        #~ raise AttributeError("%s has no attribute %r" % (self,name))


def resolve_model(model_spec, app_label=None, strict=False):
    """Return the class object of the specified model.  This works also in
    combination with :attr:`ad.Site.override_modlib_models`, so you
    don't need to worry about where the real class definition is.
    
    Attention: this function **does not** trigger a loading of
    Django's model cache, so you should not use it at module-level
    unless you know what you do.
    
    For example, ``dd.resolve_model("contacts.Person")`` will return
    the `Person` model even if the concrete Person model is not
    defined in :mod:`lino.modlib.contacts.models` because it is in
    :attr:`dd.Site.override_modlib_models`.
    
    See also django.db.models.fields.related.add_lazy_relation()

    """
    # ~ models.get_apps() # trigger django.db.models.loading.cache._populate()
    if isinstance(model_spec, basestring):
        if '.' in model_spec:
            app_label, model_name = model_spec.split(".")
        else:
            model_name = model_spec

        if AFTER17:
            from django.apps import apps
            model = apps.get_model(app_label, model_name)
        else:
            model = models.get_model(app_label, model_name, seed_cache=False)
        #~ model = models.get_model(app_label,model_name,seed_cache=seed_cache)
    else:
        model = model_spec
    if not isinstance(model, type) or not issubclass(model, models.Model):
        if strict:
            if False:
                from django.db.models import loading
                print(20130219, settings.INSTALLED_APPS)
                print(loading.get_models())
                #~ if len(loading.cache.postponed) > 0:

            if isinstance(strict, basestring):
                raise Exception(strict % model_spec)
            raise ImportError(
                "resolve_model(%r,app_label=%r) found %r "
                "(settings %s, INSTALLED_APPS=%s)" % (
                    model_spec, app_label, model,
                    settings.SETTINGS_MODULE, settings.INSTALLED_APPS))
        #~ logger.info("20120628 unresolved %r",model)
        return UnresolvedModel(model_spec, app_label)
    return model


def resolve_app(app_label, strict=False):
    """Return the `modules` module of the given `app_label` if it is
    installed.  Otherwise return either the :term:`dummy module` for
    `app_label` if it exists, or `None`.

    If the optional second argument `strict` is `True`, raise
    ImportError if the app is not installed.
    
    This function is designed for use in models modules and available
    through the shortcut ``dd.resolve_app``.
    
    For example, instead of writing::
    
        from lino.modlib.sales import models as sales
        
    it is recommended to write::
        
        sales = dd.resolve_app('sales')
        
    because it makes your code usable (1) in applications that don't
    have the 'sales' module installed and (2) in applications who have
    another implementation of the `sales` module
    (e.g. :mod:`lino.modlib.auto.sales`)

    """
    #~ app_label = app_label
    for app_name in settings.INSTALLED_APPS:
        if app_name == app_label or app_name.endswith('.' + app_label):
            return import_module('.models', app_name)
    try:
        return import_module('lino.modlib.%s.dummy' % app_label)
    except ImportError:
        if strict:
            #~ raise
            raise ImportError("No app_label %r in %s" %
                              (app_label, settings.INSTALLED_APPS))


def require_app_models(app_label):
    return resolve_app(app_label, True)

def get_field(model, name):
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

    def __init__(self, name):
        self.name = name
        self.verbose_name = "Unresolved Field " + name


def resolve_field(name, app_label=None):
    """
    Returns the field descriptor specified by the string `name` which 
    should be either `model.field` or `app_label.model.field`.
    """
    l = name.split('.')
    if len(l) == 3:
        app_label = l[0]
        del l[0]
    if len(l) == 2:
        # print "models.get_model(",app_label,l[0],False,")"
        #~ model = models.get_model(app_label,l[0],False)
        model = models.get_model(app_label, l[0])
        if model is None:
            raise FieldDoesNotExist("No model named '%s.%s'" %
                                    (app_label, l[0]))
        fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        #~ try:
            #~ fld, remote_model, direct, m2m = model._meta.get_field_by_name(l[1])
        #~ except FieldDoesNotExist:
            #~ return UnresolvedField(name)
        assert remote_model is None or issubclass(model, remote_model), \
            "resolve_field(%r) : remote model is %r (expected None or base of %r)" % (
                name, remote_model, model)
        return fld
    raise FieldDoesNotExist(name)
    #~ return UnresolvedField(name)


def get_model_report(model):
    if not hasattr(model, '_lino_default_table'):
        raise Exception("%r has no _lino_default_table" % model)
    return model._lino_default_table


def navinfo(qs, elem):
    """
    Return a dict with navigation information for the given model 
    instance `elem` within the given queryset. 
    The dictionary contains the following keys:
    
    :recno:   row number (index +1) of elem in qs
    :first:   pk of the first element in qs (None if qs is empty)
    :prev:    pk of the previous element in qs (None if qs is empty)
    :next:    pk of the next element in qs (None if qs is empty)
    :last:    pk of the last element in qs (None if qs is empty)
    :message: text "Row x of y" or "No navigation"
    
    
    """
    first = None
    prev = None
    next = None
    last = None
    recno = 0
    message = None
    #~ LEN = ar.get_total_count()
    if isinstance(qs, list):
        LEN = len(qs)
        id_list = [obj.pk for obj in qs]
        #~ logger.info('20130714')
    else:
        LEN = qs.count()
        # this algorithm is clearly quicker on queries with a few thousand rows
        id_list = list(qs.values_list('pk', flat=True))
    if LEN > 0:
        """
        Uncommented the following assert because it failed in certain circumstances 
        (see `/blog/2011/1220`)
        """
        #~ assert len(id_list) == ar.total_count, \
            #~ "len(id_list) is %d while ar.total_count is %d" % (len(id_list),ar.total_count)
        #~ print 20111220, id_list
        try:
            i = id_list.index(elem.pk)
        except ValueError:
            pass
        else:
            recno = i + 1
            first = id_list[0]
            last = id_list[-1]
            if i > 0:
                prev = id_list[i - 1]
            if i < len(id_list) - 1:
                next = id_list[i + 1]
            message = _("Row %(rowid)d of %(rowcount)d") % dict(
                rowid=recno, rowcount=LEN)
    if message is None:
        message = _("No navigation")
    return dict(
        first=first, prev=prev, next=next, last=last, recno=recno,
        message=message)
