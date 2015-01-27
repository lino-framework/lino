.. _app_inheritance:

==================
Plugin inheritance
==================

**Plugin inheritance** is a series of guidelines and programming
patterns used by Lino's :mod:`lino.modlib` and possibly other plugin
libraries.

A **plugin library** is a collection of reusable plugins which are
designed to work together.


Let's take :ref:`faggio`.  It uses Lino's standard calendar module
:mod:`lino.modlib.cal`, but extends the `Room` model defined there:

- it adds two fields `tariff` and `calendar`
- it adds another base class (the :class:`ContactRelated
  <lino.modlib.contacts.models.ContactRelated>` mixin)
- it overrides the `__unicode__` method

Here is the relevant application developer's code which defines the
*Faggio* version of :class:`cal.Room <lino_faggio.cal.models.Room>`::

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
<lino.modlib.cal.models.Room>` must have `abstract=True`.  Here is how
that class is begin defined::

    class Room(dd.BabelNamed):
        class Meta:
            abstract = dd.is_abstract_model('cal.Room')
            verbose_name = _("Room")
            verbose_name_plural = _("Rooms")


The *abstractness of certain models* in a library app must be
*optional*.  Not all Lino applications who use the calendar module
want to override the `Room` model.  Afaics there is no way in Django
to make a model abstract "afterwards".  IOW we need a central place
where models modules can ask whether it wants a given model to be
abstract or not.

This is why the above code calls the :meth:`is_abstract_model
<lino.core.site.Site.is_abstract_model>` method.  The implementation
of this method has evolved in time.  The first implementation used a
simple set of strings in a class attribute of
:class:`lino.core.site.Site`.  That might have been a standard Django
setting.  But as things got more and more complex, it became difficult
to define this manually. And it was redundant because every app *does*
know which library models it is going to override.  But how to load
that information from an app before actually importing it?  I then
discovered that Django doesn't use the :file:`__init__.py` files of
installed apps.  And of course I was lucky to have a
:class:`lino.core.site.Site` class which is being *instantiated*
before `settings` have finished to load...

The trick here is that the :file:`lino_faggio/cal/__init__.py` file
now contains this information in the `extends_models` attribute::


    from lino.modlib.cal import Plugin

    class Plugin(Plugin):

        extends_models = ['cal.Room']



The :mod:`lino.api.ad` module.

Fixtures and management commands
================================

What needs special handling when doing app inheritance are the
fixtures and the management commands.

For `fixtures` I currently use the workaround of creating one module
for every fixture of the parent, and importing `objects` from the
parent fixture.  For example the `lino_faggio/cal/fixtures` directory
imports `lino/apps/cal/fixtures`.

A similar approach would probably necessary for management commands.
Django discovers them by checking whether the app module has a
submodule "management" and then calling :meth:`os.listdir` on that
module's "commands" subdirectory.  (See Django's
:file:`core/management/__init__.py` file.)

