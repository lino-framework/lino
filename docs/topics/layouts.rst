============
Form Layouts
============

This is the topic overview about Form Layouts
which supposes that you have read the 
tutorial: :doc:`/tutorials/layouts`.

.. currentmodule:: lino.core.layouts

Overview
--------

A :class:`Layout <BaseLayout>` is an abstract pythonical description 
of how to arrange the fields and other elements of a form.

Application programmers write Layouts by subclassing
:class:`dd.FormLayout <FormLayout>`
and setting the 
:attr:`detail_layout <lino.core.actors.Actor.detail_layout>`
(or 
:attr:`insert_layout <lino.core.actors.Actor.insert_layout>`)
attribute of an :attr:`Actor <lino.core.actors.Actor>` subclass.

For simple form layouts it is enough to specify just a 
string template. See :ref:`lino.tutorial.polls`.

**A Layout consists of "panels".**
Each panel is a class attribute defined on your subclass,
containing a string value to be used as 
template describibing the content of that panel.
A Layout must define at least a ``main`` panel. 
It can define more panels whose names 
may be chosen by the application developer
(just don't chose the name :attr:`window_size` 
which has a special meaning, and don't start you panel 
names with an underscore because these are reserved for internal use).

A layout template (the value of a panel attribute) 
is a string containing words, where each word is 
either the name of a *data element*, 
or the name of another panel.

**Data elements** are database fields, table fields or :term:`slave tables <slave table>`
(except for a :class:`ParamsLayout`, where data elements are names of 
:attr:`parameters <lino.core.actors.Actor.parameters>`
defined on the actor.

Panels are **either horizontal or vertical**, 
depending on whether their template contains 
at least one newline character or not.

Indentation doesn't matter.

If the `main` panel of a :class:`FormLayout` is horizontal, 
ExtJS will render the Layout using as a tabbed main panel. 
If you want a horizontal main panel instead, just insert 
a newline somewhere in your main's template. Example::


  class NoteLayout(dd.FormLayout):
      left = """
      date type subject 
      person company
      body
      """
      
      right = """
      uploads.UploadsByController
      cal.TasksByController
      """
      
      # the following will create a tabbed main panel:
      
      main = "left:60 right:30"
      
      # to avoid a tabbed main panel, specify:
      main = """
      left:60 right:30
      """

A :class:`ListLayout` is a special case for describing the columns of a GridPanel
and therefore may contain only one `main` panel descriptor 
which must be horizontal.
ListLayouts are created automatically by Lino, using the 
:attr:`column_names <lino.core.actors.Actor.column_names>` 
attribute of the Actor as `main` panel.

A :class:`ParamsLayout` is a special case for 
describing the layout of a parameters panel.

Some blog entries with more examples of layout definition:

- :blogref:`20120630`

Modifying layouts
-----------------

- :meth:`lino.core.actors.Actor.add_detail_tabpanel`
- :meth:`lino.core.actors.Actor.set_detail_layout`
- :meth:`lino.core.actors.Actor.set_insert_layout`
