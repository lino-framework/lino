.. _lino.admin.excerpts:

=================================
Introduction to database excerpts
=================================

While the basics about printing out of a Lino application are
described in :doc:`printable`, many Lino applications use
:mod:`lino.modlib.excerpts`.

.. currentmodule:: lino.modlib.excerpts

What is a database excerpt?
===========================

A **database excerpt** is a database object which represents the fact
that a given user has requested a printable document of a given type
at a given moment.  Lino keeps all these requests in a global database
table defined by the :mod:`excerpts.Excerpt
<lino.modlib.excerpts.models.Excerpt>` model.

Users can see a history of these database excerpts using the following
menu commands:

- :menuselection:`Office --> My excerpts`
- :menuselection:`Explorer --> All excerpts`

Excerpt types
=============

Lino also has a table of **excerpt types** where the system
administrator can configure which types of database excerpts are
available on a site. You can see this list via

- :menuselection:`Configuration --> Excerpt types`

The detailed structure of this table is documented on the
:mod:`excerpts.ExcerptType <lino.modlib.excerpts.models.ExcerptType>`
model.

When a Lino process starts up, it automatically reads this table and
installs a "Print" action on every model of a site for which there
is an *excerpt type*.

Main template versus body template
==================================

In addition to the main template, excerpt types can specify a **body
template**. 
Before rendering the main template, Lino 
When the main template is being rendered, it has a context
variable ``body`` which 



Editing the main template
=========================

As a :class:`SiteAdmin <lino.core.roles.SiteAdmin>` user (and when
:mod:`lino.modlib.davlink` is installed) you can easily modify the
main template which has been used to print a given excerpt using the
:class:`Edit Template <lino.mixins.printable.EditTemplate>` button in
the detail window of that :class:`Excerpt
<lino.modlib.excerpts.models.Excerpt>` object.

Selecting the main template
===========================

If you want to configure *which* document to use as main template,
then you must use the `Configuration` menu:

- :menuselection:`Configuration --> Excerpt types`


The default main template
=========================

Lino has a main template named :xfile:`excerpts/Default.odt` which is 

.. xfile:: excerpts/Default.odt

This template is the default value, used by many excerpt types in
their :attr:`template
<lino.modlib.excerpts.models.ExcerptType.template>` field.  It is
designed to be locally overridden by local site administrators in
order to match their letter paper.



