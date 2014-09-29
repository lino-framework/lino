============
Model mixins
============

.. currentmodule:: dd

This section documents subclasses of Django's `Model
<https://docs.djangoproject.com/en/dev/ref/models/class/>`_ class
which are available in the :mod:`dd` module.


.. contents:: 
   :local:
   :depth: 2


Model
=====

.. class:: Model

  Lino adds a series of features to Django's Model base class.  If a
  Lino application includes plain Django Model classes, Lino will
  "extend" these by adding the attributes and methods defined here to
  these classes.

  .. method:: full_clean

    This is defined by Django.

  .. method:: before_ui_save(ar)

    A hook for adding customized code to be executed each time an
    instance of this model gets updated via the user interface and
    **before** the changes are written to the database.

  .. method:: after_ui_save(ar)

    Like :meth:`before_ui_save`, but 
    **after** the changes are written to the database.
    
  .. method:: after_ui_create(ar)

    Like :meth:`after_ui_save`, but only on a **new** instance.  

    Usage example: the :class:`ml.households.Household` model in
    :ref:`welfare` overrides this in order to call its `populate`
    method.


  .. method:: get_system_note_type(self, ar, silent)

    Used when :mod:`lino.modlib.notes` is installed. Expected to
    return either `None` (the default) or an existing
    :class:`ml.notes.NoteType` instance. If this is not `None`, then
    the system note will also be stored in the database as a
    :class:`ml.notes.Note`.

  .. method:: get_system_note_recipients(self, ar, silent)

    Return a list of email recipients for a system note on this
    object. Used by :meth:`rt.ActionRequest.add_system_note`.

    Every recipient must be a string with a valid email recipient like
    "john@example.com" or "John Doe <john@example.com>".


  .. method:: summary_row(self, ar)

    Return a HTML fragment that describes this record in a 
    :func:`lino.core.tables.summary`.
  
    Example::
  
        def summary_row(self, ar):
            elems = [ar.obj2html(self)]
            if self.city:
                elems. += [" (", ar.obj2html(self.city), ")"]
            return E.p(*elems)

  .. method:: get_print_language(self)

     Return a Django language code to be activated when an instance of
     this is being printed.
     The default implementation returns the Site's default language.

  .. method:: get_print_recipient(self)

     Return either `None` or an :class:`Addressable` object (usually a
     :class:`ml.contacts.Partner` instance) which is to be used as
     recipient when an instance of this is being printed.  Print
     templates

  .. method:: disable_delete(self, ar)

    Hook to decide whether a given record may be deleted.  
    Return a  non-empty string 
    
    This should return `None` if it is okay to delete this object, or
    otherwise a nonempty string with a message that explains why this
    object cannot be deleted.

    Example::
    
      def disable_delete(self,request):
          if self.is_imported:
              return _("Cannot delete imported records.")
            
    The argument `ar` contains the :class:`rt.ActionRequest` 
    which is trying to delete. `ar` is possibly `None` when this is 
    being called from a script or batch process.


  .. method:: define_action(cls, **kwargs)

    Adds one or several actions to this model.
    Actions must be specified using keyword arguments.

    Used e.g. by :mod:`lino.modlib.cal` to add the `UpdateReminders`
    action to :class: `lino.modlib.users.models.User`.

  .. method:: disabled_fields(self, ar)

    Return a list of names of fields that should be disabled (not editable) 
    for this record.
    
    Example::
    
      def disabled_fields(self,request):
          if self.user == request.user: return []
          df = ['field1']
          if self.foo:
            df.append('field2')
          return df
        

  .. method:: hide_elements(cls, *names)

    Mark the named data elements (fields) as hidden.  They remain in
    the database but are not visible in the user interface.

  .. method:: on_create(self, ar)

    Used e.g. by :class:`ml.notes.Note`.
    on_create gets the action request as argument.
    Didn't yet find out how to do that using a standard Django signal.

  .. method:: before_ui_save(self, ar)

    Called after a PUT or POST on this row, and before saving the row.

    Example in :class:`ml.cal.Event` to mark the event as user
    modified by setting a default state.

  .. method:: after_ui_save(self, ar)

    Called after a PUT or POST on this row, 
    and after the row has been saved.
    Used by 
    :class:`lino_welfare.modlib.debts.models.Budget` 
    to fill default entries to a new Budget,
    or by :class:`lino_welfare.modlib.cbss.models.CBSSRequest` 
    to execute the request,
    or by 
    :class:`lino_welfare.modlib.jobs.models.Contract` 
    :class:`lino_welfare.modlib.pcsw.models.Coaching` 
    :class:`lino.modlib.vat.models.Vat` 

  .. method:: get_row_permission(self, ar, state, ba)

    Returns True or False whether this row instance gives permission
    to the ActionRequest `ar` to run the specified action.

  .. method:: setup_table(cls, t)

    Called during site startup once on each Table that 
    uses this model.

  .. method:: on_duplicate(self, ar, master)

    Called by :meth:`lino.mixins.duplicable.Duplicable.duplicate`.
    `ar` is the action request that asked to duplicate.
    If `master` is not None, then this is a cascaded duplicate initiated
    be a duplicate() on the specifie `master`.


  .. method:: FOO_choices

    Return a queryset or list of allowed choices for field FOO.

    For every field named "FOO", if the model has a method called
    "FOO_choices" (which must be decorated by :func:`dd.chooser`),
    then this method will be installed as a chooser for this field.

    Example of a context-sensitive chooser method::
  
      country = models.ForeignKey("countries.Country", blank=True, null=True)
      city = models.ForeignKey('countries.City', blank=True, null=True)
          
      @chooser()
      def city_choices(cls,country):
          if country is not None:
              return country.place_set.order_by('name')
          return cls.city.field.rel.to.objects.order_by('name')
      
  


  .. method:: FOO_changed

    Called when field FOO of an instance of this model has been
    modified through the user interface.

    For every field named "FOO", if the model has a method called
    "FOO_changed", then this method will be installed as a field-level
    post-edit trigger.

    Example::
    
      def city_changed(self,oldvalue):
          print("City changed from %s to %s!" % (oldvalue, self.city))

  .. attribute:: active_fields

    Default value for :attr:`dd.Table.active_fields`


  .. attribute:: allow_cascaded_delete

    A list of names of ForeignKey fields of this model that allow for
    cascaded delete.
    
    When deleting an object through the user interface, Lino by
    default forbids to delete an object that is referenced by other
    objects. Users will get a message of type "Cannot delete X because
    n Ys refer to it".
    
    Example: Lino should not refuse to delete a Mail just because it
    has some Recipient.  When deleting a Mail, Lino should also delete
    its Recipients.  That's why
    :class:`lino.modlib.outbox.models.Recipient` has
    ``allow_cascaded_delete = ['mail']``.
    
    Note that this currently is also consulted by
    :meth:`lino.mixins.duplicable.Duplicable.duplicate` to decide
    whether slaves of a record being duplicated should be duplicated
    as well.
    
    This mechanism doesn't depend on nor influence Django's `on_delete
    <https://docs.djangoproject.com/en/dev/ref/models/fields/#django.db.models.ForeignKey.on_delete>`_
    option.  But of course you should not allow_cascaded_delete for
    fields which have e.g. `on_delete=PROTECT`.


  .. method:: print_subclasses_graph

    Returns an internationalized `graphviz` directive representing
    the polymorphic forms of this model.

    Usage example::

      .. django2rst:: 

          with dd.translation.override('de'):
              contacts.Partner.print_subclasses_graph()

Polymorphic
===========

.. class:: Polymorphic

    Mixin for models that use Multiple Table Inheritance to implement
    polymorphism.  

    Subclassed e.g. by :class:`ml.contacts.Partner`: the recipient of
    an invoice can be a person, a company, a client, a job provider,
    an employee...). A given partner can be both a person and an
    employee at the same time.

    Note that not every usage of Multiple Table Inheritance means
    polymorphism. For example :class:`ml.ledger.Voucher` has a pointer
    to the journal which knows which specialization to use.  A given
    voucher has always exactly one specialization.

    Implemented in :mod:`lino.mixins.polymorphic`.

Addressable
===========

.. class:: Addressable

    Interface (abstract base class) to encapsulates the generating of
    "traditional" ("snail") mail addresses.  

    It differentiates between the "person" and the "location" part of
    an address.  For example::
    
        Mr. Luc Saffre     | person
        Rumma & Ko OÜ      | person
        Uus 1              | location
        Vana-Vigala küla   | location
        ...                | location

    .. method:: address_person_lines(self)

        Expected to yield one or more unicode strings, one for each line
        of the person part.

    .. method:: address_location_lines(self)

        Expected to yield one or more unicode strings, one for each line
        of the location part.

    .. method:: get_address(self, linesep="\n")

        The plain text full postal address (person and location). 
        Lines are separated by `linesep`.

    .. attribute:: address

        A property which calls :meth:`get_address`.

    .. attribute:: address_html

        A property which calls :meth:`get_address_html`.
    
    .. method:: get_address_html(self, **attrs)

        Returns the full postal address a a string containing html 
        markup of style::
        
            <p>line1<br />line2...</p>
          
        Optional attributes for the enclosing `<p>` tag can be 
        specified as keyword arguments. Example::

            >>> from lino import dd
            >>> class MyAddr(dd.Addressable):
            ...     def __init__(self, *lines): self.lines = lines
            ...     def address_person_lines(self): return []
            ...     def address_location_lines(self): return self.lines
            ...     
            >>> addr = MyAddr('line1','line2')
            >>> print(addr.get_address_html(class_="Recipient"))
            <p class="Recipient">line1<br />line2</p>
          
        See :mod:`lino.utils.xmlgen.html`.

Born
====          

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

Human
=====


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

Printable
=========

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


CachedPrintable
===============

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

TypedPrintable
==============

.. class:: TypedPrintable

    A :class:`CachedPrintable` that uses a "Type" for deciding which
    template to use on a given instance.
    
    A TypedPrintable model must define itself a field ``type`` which
    is a ForeignKey to a Model that implements :class:`PrintableType`.
    
    Alternatively you can override :meth:`get_printable_type` if you
    want to name the field differently. An example of this is
    :attr:`ml.sales.SalesDocument.imode`.


PrintableType
=============

.. class:: PrintableType

    Base class for models that specify the
    :attr:`TypedPrintable.type`.
