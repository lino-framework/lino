===================
Old changes in Lino
===================

Version 1.7.4 (released :blogref:`20160712`)
============================================

Bugfix release.


Version 1.7.3 (released :blogref:`20160712`)
============================================

This is the first time we release three projects at the same time and
using the same version number: :ref:`lino`, :ref:`xl` and :ref:`book`.

- New module :mod:`lino.sphinxcontrib.help_text_builder`
  (:blogref:`20160620`).

- When merging database objects (:mod:`lino.core.merge`), Lino did not
  care at all about objects related to the MTI parents. For example,
  when merging two participants, then it redirects their enrolments
  but not e.g. their invoices, bank statements (i.e. objects pointing
  to this participant as person or partner).
  (:blogref:`20160621`)

- New site attribute :attr:`lino.core.site.Site.workflows_module`.
  Lino no longer executes any `setup_workflows`
  callable. (:blogref:`20160622`)


Lino XL 1.0.0 (released :blogref:`20160705`)
============================================

The first release on PyPI of the :ref:`xl` which is being used as a
clone of the GitHub repository on our production sites since its
creation.


Lino 1.7.2 (released :blogref:`20160619`)
=========================================

- Lino now supports Django's generic relations (`GenericRelation
  <https://docs.djangoproject.com/ja/1.9/ref/contrib/contenttypes/#reverse-generic-relations>`_).  (:blogref:`20160523`)

- Error messages of style :message:`NotImplementedError: <dl> inside
  <text:p>` are now being shown correctly in the alert box for the
  user.  (:blogref:`20160523`)

- When duplicating a database object, Lino now calls the
  :meth:`on_duplicate <lino.core.model.Model.on_duplicate>` method on
  the master *before* saving it for a first time. (:blogref:`20160523`)

- New build method :mod:`lino.modlib.weasyprint`.

- :class:`CustomBuildMethod
  <lino.modlib.printing.utils.CustomBuildMethod>` : a new style of
  build method for printables which have a target file to be
  generated, but don't use any template. (:blogref:`20160512`)

- :attr:`lino.core.site.Site.default_ui` is now the
  full Python name, not just the app_label. (:blogref:`20160506`)

- Added `CachedPrintableChecker
  <lino.modlib.printing.mixins.CachedPrintableChecker>` which checks
  for missing cache files (:blogref:`20160427`, :blogref:`20160504`).

- And quite some other.

Version 1.7.0 (released :blogref:`20160426`)
============================================

Important changes which caused a minor version bump:

- Lino no longer requires an old Python version (:ticket:`36`)
- Lino no longer requires an old Django version (:ticket:`38` and :ticket:`650`)
- Moved "enterprise" plugins from :mod:`lino.modlib` to :ref:`xl`
  (:ticket:`356`)
- Moved "Accounting" plugins from :mod:`lino.modlib` to :ref:`cosi`
  (:ticket:`520`)

- Lots of optimizations and bugfixes

- The :attr:`username <lino.modlib.users.models.User.username>` of a
  user is now nullable (can be empty). :blogref:`20160425`.



Version 1.6.19 (released :blogref:`20150901`)
=============================================

- Changed Development Status from beta to stable.
- Lots of changes, especially the murder bug (:blogref:`20150831`)


Version 1.6.18 (released :blogref:`20150728`)
=============================================

- Lots of changes. Lino Noi 0.0.1 needs this version.

- When :meth:`lino.core.actions.Action.run_from_ui` raises an
  exception, Lino (until now) nevertheless closed the action form
  window. Now the window is closed only when the action runs without
  any exception. :blogref:`20150226`.

- Building the :xfile:`lino_*.js` files (:mod:`lino.utils.jsgen`) is
  now thread-safe.  :blogref:`20150225`.

- No more need to set `user_model` :blogref:`20150116`.

- New way to define modular menus. :blogref:`20150114`.

- :class:`ShowSlaveTable <lino.core.actions.ShowSlaveTable>` did not
  yet copy over the :attr:`sort_index
  <lino.core.actors.Actor.sort_index>` specified on a table to the
  :attr:`sort_index <lino.core.actions.Action.sort_index>` of the
  action.  Bug fixed.



Version 1.6.17 (released :blogref:`20150108`)
=============================================

- :func:`lino.utils.mti.delete_child` was no longer working with recent
  Django versions. :blogref:`20150108`

- New feature: :mod:`lino.utils.sendchanges`.

- Miscellaneous internal changes.

- new plugin method :meth:`get_menu_group
  <lino.core.plugin.Plugin.get_menu_group>`. :blogref:`20141231`

- Documentation now builds without warnings. :blogref:`20141223`

Version 1.6.16 (released :blogref:`20141222`)
=============================================

A minor release because

- New module :mod:`lino.hello`.

- Some classes changed their place while working on :ticket:`39`

- `/dev/install` is getting better. I am working on it for
  :ticket:`40`.

Version 1.6.15 (released 2014-12-12)
====================================

- Integrated my `north <https://github.com/lsaffre/north>`_
  and `djangosite <https://github.com/lsaffre/djangosite>`_
  projects into Lino.
  These independent github projects are now obsolete and no longer
  maintained.

- A "plugin" is an app which defines in
  her `__init__.py` a class named "Plugin" which must be a subclass of
  :class:`dd.Plugin`.
  We could also call them "new-style apps".
  A Plugin can have additional configuration.

  This mechanism is also a (partial) solution for
  `Django ticket #3591 <https://code.djangoproject.com/ticket/3591>`_
  Aymeric Augustin's solution
  being imported *before* Django settings.


- The apps of a Site are later accessible via
  `settings.SITE.plugins.foo`
- Some **site** settings have become **plugin** settings:
  The are no longer defined as class attributes of `Site`, but
  defined in the `App` class.
  For example :setting:`extensible_root` is now in
  :attr:`lino.apps.extensible.App.media_root`.

- Concrete example in my :xfile:`lino_local.py`.

  Before::

    def setup_site(self):
        ...
        self.bootstrap_root = '/home/luc/snapshots/bootstrap'
        self.bootstrap_base_url = None

        self.extensible_root = '/home/luc/snapshots/extensible-1.0.1'
        self.extensible_base_url = None

        self.extjs_root = '/home/luc/snapshots/ext-3.3.1'


  After::

    def setup_site(self):
        ...
        self.configure_plugin(
            'extensible',
            calendar_start_hour=9,
            media_root='/home/luc/snapshots/extensible-1.0.1',
            media_base_url=None)

        self.configure_plugin(
            'plain',
            media_root='/home/luc/snapshots/bootstrap',
            media_base_url=None)

        self.configure_plugin(
            'extjs',
            media_root='/home/luc/snapshots/ext-3.3.1',
            media_base_url=None)


Summary:


   =============== ==========================
   Before          After
   --------------- --------------------------
   admin_prefix    plugins.extjs.url_prefix
   extjs_base_url  plugins.extjs.media_base_url
   extjs_root      plugins.extjs.media_root
   =============== ==========================



- :mod:`lino.apps.extjs` and
  :mod:`lino.apps.plain`
  are now plugins.
  They are currently being included automatically in
  :meth:`lino.lino_site.Site.get_installed_apps`
  to avoid more code changes in existing applications.

- Moved `lino.extjs` to `lino.apps.extjs`



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

  - New command :cmd:`fab test_sdist` (:blogref:`20130913`).

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
  :class:`lino.core.actions.Action <lino.core.actions.Action>`.


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


.. toctree::

    16.10


.. toctree::
    :hidden:

    marked_changes


