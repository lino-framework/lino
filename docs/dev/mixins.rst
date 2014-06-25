============
Model mixins
============

.. currentmodule:: dd


.. class:: Born

    Abstract base class that adds a `birth_date`
    field and a virtual field "Age".

  .. attribute:: birth_date


  .. attribute:: age

    Virtual field, displays the age in years.

  .. method:: get_age(self, ar, today=None)

    Return the age as a :class:`datetime.timedelta` object.

    `ar` is the requesting :class:`ActionRequest` which can be `None`
    because it is ignored.
    
    Optional keyword argument `today` should be a
    :class:`datetime.date` instance to replace the actual current
    date. This is used if you want the age at a given date in the past
    or the future.
    The default value calls :meth:`dd.Site.today`.



.. class:: Human

  Base class for all models that represent a human.  It defines the
  fields `first_name`, `middle_name, `last_name` and `gender`.

  .. attribute:: first_name

    The first name, also known as given name.

  .. attribute:: last_name

    The last name, also known as family name.

  .. attribute:: middle_name

    A space-separated list of all `middle names
    <http://en.wikipedia.org/wiki/Middle_name>`_.

  .. attribute:: gender

    The gender of this person. 
    Possible values are defined in :class:`dd.Genders`.


  .. method:: mf(self, m, f, u=None)

    Taking three parameters `m`, `f` and `u` of any type, returns one
    of them depending on whether this Person is male, female or of
    unknown gender.

    See :ref:`lino.tutorial.human` for some examples.


  .. method:: get_full_name(self, salutation=True,
                            upper=None, **salutation_options)

    Returns a one-line string composed of salutation,
    :attr:`first_name` and :attr:`last_name`.

    The optional keyword argument `salutation` can be set to
    `False` to suppress salutations.

    The optional keyword argument `upper` can be specified to
    override the Site's default value
    (:setting:`uppercase_last_name`). `True` means to convert the
    last name to uppercase as is usually done in French.

    Any other keyword arguments are forwarded to
    :func:`lino.mixins.human.get_salutation` (see there).

    See :ref:`lino.tutorial.human` for some examples.


.. class:: Printable

    Mixin for Models whose instances have a "print" action (i.e. for
    which Lino can generate a printable document).

    Extended by :class:`CachedPrintable` and :class:`TypedPrintable`.
    
    .. method:: get_print_templates(self, bm, action)

        Return a list of filenames of templates for the specified
        build method.  Returning an empty list means that this item is
        not printable.  For subclasses of :class:`SimpleBuildMethod`
        the returned list may not contain more than 1 element.

    .. method:: get_printable_context(self, ar, **kw)

        Defines certain names of a template context.
        See :doc:`/user/templates_api`.
        :class:`ml.notes.Note` extends this.


.. class:: CachedPrintable

    Mixin for Models that generate a unique external file at a
    determined place when being printed.
    
    Adds a "Print" button, a "Clear cache" button and a `build_time`
    field.
    
    The "Print" button of a :class:`CachedPrintable
    <lino.mixins.printable.CachedPrintable>` transparently handles the
    case when multiple rows are selected.  If multiple rows are
    selected (which is possible only when :attr:`cell_edit
    <lino.core.tables.AbstractTable.cell_edit>` is True), then it will
    automatically:
    
    - build the cached printable for those objects who don't yet have
      one
      
    - generate a single temporary pdf file which is a merge of these
      individual cached printable docs

    .. attribute:: build_time

        Timestamp of the built target file. Contains `None`
        if no build hasn't been called yet.

.. class:: TypedPrintable

    A :class:`CachedPrintable` that uses a "Type" for deciding which
    template to use on a given instance.
    
    A TypedPrintable model must define itself a field ``type`` which
    is a ForeignKey to a Model that implements :class:`PrintableType`.
    
    Alternatively you can override :meth:`get_printable_type` if you
    want to name the field differently. An example of this is
    :attr:`ml.sales.SalesDocument.imode`.



.. class:: PrintableType

    Base class for models that specify the
    :attr:`TypedPrintable.type`.
