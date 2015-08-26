========================
GenericForeignKey fields
========================

The `GenericForeignKey` field (GFK) is a great feature provided by
Django's `django.contrib.contenttypes
<https://docs.djangoproject.com/en/1.6/ref/contrib/contenttypes/>`_
module. While a normal `ForeignKey` field can point to a database
object *of a given model*, a `GenericForeignKey` can point to a
database object *of any model*.

This section provides a topic overview. See also
:doc:`/tutorials/gfktest/index` and
:mod:`test_broken_gfks <lino_welfare.projects.eupen.tests.test_broken_gfks>`).

Lino's :meth:`disable_delete <lino.core.model.Model.disable_delete>`
method tests for related objects, which automatically includes also
those which are related using a GFK. non-nullable and warning before
message.

In order to use GFKs, you must have ``django.contrib.contenttypes`` in
your :setting:`INSTALLED_APPS`. In a Lino application we recommend to
use :mod:`lino.modlib.contenttypes`, which is a thin wrapper around
Django's original app. Lino's version gives you additional
functionality:

- the :class:`Controllable <lino.modlib.gfks.mixins.Controllable>`
  model mixin 
- the :class:`BrokenGFKs <lino.modlib.gfks.models.BrokenGFKs>` table

In Lino you can configure the cascading behaviour *from the model
which defines the GFK*, either by using the
:attr:`allow_cascaded_delete
<lino.core.model.Model.allow_cascaded_delete>` attribute or by
defining a nullable GFK.

