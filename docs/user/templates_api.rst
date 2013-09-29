=====================
Template designer API
=====================

TODO: This is just a start and far from being complete...


.. glossary::
    :sorted:

    ``this``
        The printable object instance
        
    ``mtos``
        "amount to string" using :func:`decfmt`
        
    ``fds``
        "format date short", see :ref:`datefmt`
        
    ``fdm``
        "format date medium", see :ref:`datefmt`
            
    ``fdl``
        "format date long", see :ref:`datefmt`
            
    ``fdf``
        "format date full", see :ref:`datefmt`
            
            
    ``iif``
        :func:`iif <atelier.utils.iif>`
        
    ``tr(**kw)``
        Shortcut to :meth:`babelitem <north.Site.babelitem>`.
        
    ``_(s)``
        gettext
        
    ``E``
        HTML tag generator, see :mod:`lino.utils.xmlgen.html`
        
    ``unicode()``
        the builtin Python :func:`unicode` function
        
    ``len()``
        the builtin Python :func:`len` function

    ``settings``  
        The Django :xfile:`settings.py` module

    ``site`` 
        shortcut for `settings.SITE`
        
    ``dtos``
        deprecated for :term:`fds`
        
    ``dtosl``
        deprecated for :term:`fdl`

    ``ar``
        a Lino :class:`lino.core.requests.BaseRequest` instance around 
        the calling Django request 


    ``request`` 
        the Django HttpRequest instance
        (available in :xfile:`admin_main.html`,
        rendered by :meth:`get_main_html <lino.ui.Site.get_main_html>`,
        which calls :func:`lino.core.web.render_from_request`)
        


.. initialization for doctest

    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.cosi.settings.test'
    >>> from lino.runtime import *
    >>> from north.dbutils import fds,fdm,fdl,fdf
    >>> import datetime


.. _datefmt:

Date formatting functions
-------------------------

Lino includes shortcuts to `python-babel`'s 
`date formatting functions <http://babel.pocoo.org/docs/dates/>`_:

>>> d = datetime.date(2013,8,26)
>>> print(fds(d)) # short
8/26/13
>>> print(fdm(d)) # medium
Aug 26, 2013
>>> print(fdl(d)) # long
August 26, 2013
>>> print(fdf(d)) # full
Monday, August 26, 2013
