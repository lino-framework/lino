.. _app_inheritance:

==================
Plugin inheritance
==================

**Plugin inheritance** is a series of guidelines and programming
patterns used by Lino's :mod:`lino.modlib` and possibly other plugin
libraries.

A **plugin library** is a collection of reusable plugins which are
designed to work together.

The :mod:`lino.projects.min2` project has an example of extending a
plugin from  :mod:`lino.modlib`.


The :meth:`is_abstract_model` method
====================================

Let's take :ref:`voga`.  It uses Lino's standard calendar module
:mod:`lino.modlib.cal`, but extends the `Room` model defined there:

- it adds two fields `tariff` and `calendar`
- it adds another base class (the :class:`ContactRelated
  <lino.modlib.contacts.models.ContactRelated>` mixin)
- it overrides the `__unicode__` method

Here is the relevant application developer's code which defines the
*Voga* version of :class:`cal.Room <lino_voga.cal.models.Room>`::

    from lino.modlib.cal.models import Room
    from lino.modlib.contacts.models import ContactRelated

    class Room(Room, ContactRelated):

        tariff = dd.ForeignKey('products.Product', ...)
        calendar = dd.ForeignKey('cal.Calendar', ...)

        def __unicode__(self):
            s = dd.BabelNamed.__unicode__(self)
            if self.company and self.company.city:
                s = '%s (%s)' % (self.company.city, s)
            return s

For this to work, the *library version* of :class:`cal.Room
<lino.modlib.cal.models.Room>` must have `abstract=True`.  But only in
this special case. The general case is that when an application
installs :mod:`lino.modlib.cal` , it gets (among others) a new model
:class:`cal.Room <lino.modlib.cal.models.Room>`.  We wouldn't want to
force every application which uses :mod:`lino.modlib.cal` to override
the `Room` model just to make it concrete.

In other words: The *abstractness of certain models* in a library
plugin must be *optional*.  The plugin developer should need to decide
whether his version of the Model is subclassable or not.

There is no way in Django to make a model abstract "afterwards".  So
we need a central place where models modules can ask whether it wants
a given model to be abstract or not.

To solve this problem, Lino offers the :meth:`is_abstract_model
<lino.core.site.Site.is_abstract_model>` method.  Usage example::

    class Room(dd.BabelNamed):
        class Meta:
            abstract = dd.is_abstract_model(__name__, 'Room')
            verbose_name = _("Room")
            verbose_name_plural = _("Rooms")

The trick here is that the :file:`lino_voga/lib/cal/__init__.py` file
now contains this information in the `extends_models` attribute::


    from lino.modlib.cal import Plugin

    class Plugin(Plugin):

        extends_models = ['Room']


The implementation of :meth:`is_abstract_model
<lino.core.site.Site.is_abstract_model>` has evolved in time.  The
first implementation used a simple set of strings in a class attribute
of :class:`lino.core.site.Site`.  That might have been a standard
Django setting.  But as things got more and more complex, it became
difficult to define this manually. And it was redundant because every
app *does* know which library models it is going to override.  But how
to load that information from an app before actually importing it?  We
then discovered that Django doesn't use the :file:`__init__.py` files
of installed apps.  And of course we were lucky to have a
:class:`lino.core.site.Site` class which is being *instantiated*
before `settings` have finished to load...


See also the :mod:`lino.api.ad` module.

The `config` directory
======================

The `config` subdirectories are handled automatically as expected:
Lino scans first the `config` subdirectory of the child, then those of
the parents.

Fixtures and management commands
================================

When doing plugin inheritance, the `fixtures`, `config` and `management`
subdirs need special attention.

For `fixtures` you must create one module for every fixture of the
parent, and import at least `objects` from the parent fixture.  For
example the :mod:`lino_voga.cal.fixtures` package contains a suite
of one-line modules, one for each module in :mod:`lino.cal.fixtures`,
each of which with just one `import` statement like this::

  from lino.modlib.cal.fixtures.demo import objects

A similar approach would probably necessary for django-admin commands.
Django discovers them by checking whether the app module has a
submodule "management" and then calling :meth:`os.listdir` on that
module's "commands" subdirectory.  (See Django's
:file:`core/management/__init__.py` file.)

