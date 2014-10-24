========
Excerpts
========

.. module:: ml.excerpts

The :mod:`lino.modlib.excerpts` package provides data definitions for
using "database excerpts".

- Lino automatically installs a "Print" action on every model of your
  app for which the database contains an :class:`ExcerptType`
  instance.

- Note that Lino does not automatically add an action per model to
  make the excerpt history visible from a model. If you this, add
  yourself your preferred variant. This can be either using a
  :class:`dd.ShowSlaveTable` button in the toolbar::

    show_excerpts = dd.ShowSlaveTable('excerpts.ExcerptsByOwner')
    show_excerpts = dd.ShowSlaveTable('excerpts.ExcerptsByProject')

  Or by adding :class:`excerpts.ExcerptsByOwner <ExcerptsByOwner>` or
  :class:`excerpts.ExcerptsByProject <ExcerptsByProject>` (or both, or
  your own subclass of one of them) to the
  :attr:`detail_layout <dd.Actor.detail_layout>`.




Models
------


.. class:: ExcerptType

  .. attribute:: template

    The main template to be used when printing an excerpt of this type.

  .. attribute:: content_type

    The model on which excerpts of this type are going to work.

  .. attribute:: certifying
  .. attribute:: body_template
  .. attribute:: primary
  .. attribute:: backward_compat
  .. attribute:: print_recipient
  .. attribute:: print_directly

  .. attribute:: shortcut

  Links this excerpt type to a shortcut field.
  A pointer to :class:`Shortcuts`.

  If this is not empty, then the given shortcut field will manage
  excerpts of this type.


.. class:: Excerpt

    An excerpt is a printable document that describes some aspect
    of the current situation.

  .. attribute:: owner

    :ref:`gfk` to the object being printed by this excerpt.
    Defined in :class:`dd.Controllable`.

  .. attribute:: company

    The optional recipient of this excerpt.
    (ForeignKey to :class:`ml.contacts.Company`)

  .. attribute:: contact_person

    The optional recipient of this excerpt.
    (ForeignKey to :class:`ml.contacts.Person`)

  .. attribute:: excerpt_type

  The type of this excerpt (ForeignKey to :class:`ExcerptType`).

  .. attribute:: language

  .. attribute:: date

  .. attribute:: time

  .. method:: get_address_html

  Return the address of *the recipient of this excerpt* as a string
  containing html markup.  The markup defines exactly one paragraph,
  even if this excerpt has no recipient (in which case the paragraph
  is empty).

  Any arguments are forwarded to :meth:`lines2p
  <lino.utils.xmlgen.html.lines2p>` which is used to pack the address
  lines into a paragraph.

  The "recipent of this excerpt" is either the :attr:`company` or
  :attr:`contact_person` of this excerpt (if one of these fields is
  non-empty), or the recipient of the :attr:`owner`.

  


Mixins
------

.. class:: Certifiable

  Any model which inherits from this mixin becomes "certifiable".

  That is:

    - it has a `printed_by` field and a corresponding virtual field
      `printed` which point to the excerpt that is the "definitive"
      ("Certifying") printout of this object.

    - It may define a list of "certifiable" fields. 
      See :meth:`get_certifiable_fields`.

  Usage example::

      from lino.modlib.excerpts.mixins import Certifiable

      class MyModel(dd.UserAuthored, Certifiable, dd.Duplicable):
          ...

  The :mod:`lino.modlib.excerpts.fixtures.std` fixture automatically
  creates a certifying :class:`ExcerptType` instance for every model
  which inherits from :class:`Certifiable`.
  

  .. attribute:: printed

    Displays information about when this certifiable has been printed.
    Clicking on it will display the excerpt pointed to by
    :attr:`printed_by`.

  .. attribute:: printed_by

    ForeignKey to the :class:`Excerpt` which certifies this instance.

    A :class:`Certifiable` is considered "certified" when this this is
    not `None`.

  .. method:: get_certifiable_fields()

    Expected to return a string with a space-separated list of field
    names.  These files will automaticaly become disabled (readonly)
    when the document is "certified". The default implementation
    returns an empty string, which means that no field will become
    disabled when the row is "certified".

    Example::

        @classmethod
        def get_certifiable_fields(cls):
            return 'date user title'





Tables
------

.. class:: Excerpts

  Base class for all tables on :class:`Excerpt`

.. class:: ExcerptsByOwner

  Shows all :class:`Excerpts` whose :attr:`owner <Excerpt.owner>`
  field is this.

.. class:: ExcerptsByProject


Actions
-------

.. class:: CreateExcerpt
.. class:: ClearPrinted


Choicelists
-----------

.. class:: Shortcuts


Document templates
------------------

.. xfile:: excerpts/Default.odt

This template is the default value, used by many excerpt types in
their :attr:`ExcerptType.template` field.  It is designed to be
locally overridden by local site administrators in order to match
their letter paper.



