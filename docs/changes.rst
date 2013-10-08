.. _lino.changes: 

===============
Changes in Lino
===============

I try to give here a summary of the things which system administrators 
should know when upgrading.
See the author's :ref:`Developer Blog <blog>`
to get detailed news.
The final truth about what's going on is only 
`The Source Code <http://code.google.com/p/lino/source/list>`_.

  
Version 1.6.13 (released :blogref:`20131007`)
=============================================

Some subtle bugfixes and optimizations.
Mostly because of :ref:`welfare`. 

Version 1.6.12 (released :blogref:`20130924`)
=============================================

- New framework features include 

  - customizable export as .pdf, 
    (:blogref:`20130912`).
  - menu buttons (grouped actions), see :blogref:`20130913`.
  
  - New fab command :fab:`test_sdist` (:blogref:`20130913`).
    
  - New management command :manage:`dump2py`.
  
  - The :ref:`davlink` applet now works around some permission problems
    which occured after Oracle JRE 7u21
    (:blogref:`20130919`).
  - It is now (again) possible to run multiple Lino instances on a same 
    vhost in different subdirectories. 
    See :attr:`site_prefix <lino.site.Site.site_prefix>`.

  
- Framework bugfixes include 
  (1) table parameter panel initial size
  (2) 


- Renamed `dd.AuthorRowAction` to `dd.AuthorAction`
  and merged the now obsolete `dd.RowAction` into 
  :class:`dd.Action <lino.core.actions.Action>`.


- :mod:`html2xhtml <lino.utils.html2xhtml>` is now just a wrapper to 
  `pytidylib <http://countergram.com/open-source/pytidylib>`_
  (which itself is a wrapper to `HTML Tidy <http://tidy.sourceforge.net>`_). 
  See :blogref:`20130824`.
  IOW, you will probably want to run either::
  
    $ sudo apt-get install python-tidylib
    
  or::

    $ sudo apt-get install libtidy-dev
    $ pip install pytidylib
  



Version 1.6.11 (released :blogref:`20130723`)
=============================================

- Check the new setting :attr:`is_demo_site <lino.ui.Site.is_demo_site>`
  which defaults to `True`.

- Existing Lino applications must add :mod:`lino.modlib.system`
  to the list of apps yielded by their
  :meth:`lino.ui.Site.get_installed_apps`.
  See :blogref:`20130717` for background. 
  
  Migration instructions:
  
  If you don't override the :class:`lino.ui.Site` class, then your 
  instantiating code in settings.py is something like::
  
    SITE = Site(globals(),'foo','bar')

  Change this to::
  
    SITE = Site(globals(),'lino.modlib.system','foo','bar')
    
  If you do override it, then change your `get_installed_apps` method::
  
    def get_installed_apps(self):
        for a in super(Site,self).get_installed_apps():
            yield a
        yield 'lino.modlib.system' ## <<< this line added
        yield 'lino.modlib.users'
        # continue with your own modules
        
  Also the models `SiteConfig`, `HelpText` and `TextFieldTemplate` 
  have now the app_label "system" instead of "ui".
  If you have production data, you'll need to write a data migration 
  to rename these tables. See :mod:`lino_welfare.migrate` for 
  an example on how to automate this.
  

- Optimization: 
  virtual fields to a foreignkey 
  (e.g. the new `bailiff` field in `welfare.debts.PrintLiabilitiesByBudget`)
  might cause a "unicode object has no attribute '_meta'" traceback.

  

Version 1.6.6 (released :blogref:`20130505`)
============================================

- :mod:`lino.utils.html2odf` now converts the text formats `<i>` 
  and `<em>` to a style "Emphasis".
  `<b>` is no longer converted to "Bold Text" but 
  to "Strong Emphasis".

- Lino now supports 
  :class:`lino.core.fields.RemoteField` to a 
  :class:`lino.core.fields.VirtualField`.
  See :blogref:`20130422`

- :mod:`lino.core.auth` forgot to set `request.subst_user` to `None`
  for html HEAD requests.
  (:blogref:`20130423`)
  
- Readable user message when contract type empty
  (:blogref:`20130423`)

Version 1.6.5 (released :blogref:`20130422`)
============================================

- Exceptions "Using remote authentication, but no user credentials 
  found." and "Unknown or inactive username %r. Please contact your 
  system administrator."
  raised by :class:`lino.core.auth.RemoteUserMiddleware`
  no longer is a PermissionDenied but a simple Exception.
  See :blogref:`20130409`.

- :class:`lino.core.fields.IncompleteDateField` now has a 
  default `help_text` (adapted from `birth_date` field 
  in :class:`lino.mixins.human.Born`)

- The new method :meth:`lino.core.model.Model.subclasses_graph`
  generates a graphviz directive which shows this model and the 
  submodels.
  the one and only usage example is visible in the 
  `Lino-Welfare user manual
  <http://welfare-user.lino-framework.org/fr/clients.html#partenaire>`_
  See :blogref:`20130401`.


Older releases
==============

.. toctree::
   :maxdepth: 1
   
   /releases/index
