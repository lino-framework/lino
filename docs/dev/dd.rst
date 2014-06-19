===============
Database Design
===============

The :mod:`lino.dd` module is a shortcut to those parts of Lino which
are used in your :xfile:`models.py` modules.  The name ``dd`` stands
for "Database Design".

To keep your application as future-proof as possible, you should use
these shortcuts instead of importing these classes and functions from
their real place.

.. toctree::
   :maxdepth: 2

   actors
   actions
   layouts

.. currentmodule:: dd


The `dd.Model` class
--------------------

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


  .. method:: summary_row(self, ar)

    Return a HTML fragment that describes this record in a 
    :func:`lino.core.tables.summary`.
  
    Example::
  
        def summary_row(self, ar):
            elems = [ar.obj2html(self)]
            if self.city:
                elems. += [" (", ar.obj2html(self.city), ")"]
            return E.p(*elems)


           
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


Miscellaneous functions
-----------------------

.. function:: fields_list(model, field_names)

Return a set with the names of the specified fields, checking whether
each of them exists.

**Arguments:** `model` is any subclass of `django.db.models.Model`. It
may be a string with the full name of a model
(e.g. ``"myapp.MyModel"``).  `field_names` is a single string with a
space-separated list of field names.

If one of the names refers to a :class:`DummyField`, this name
will be ignored silently.

For example if you have a model `MyModel` with two fields `foo` and
`bar`, then ``dd.fields_list(MyModel,"foo bar")`` will return
``['foo','bar']`` and ``dd.fields_list(MyModel,"foo baz")`` will raise
an exception.

.. class:: DummyField(*args, **kwargs)

Represents a field that doesn't exist in the current configuration but
might exist in other configurations.

.. class:: ForeignKey(othermodel, *args, **kwargs)

This is almost as Django's `ForeignKey
<https://docs.djangoproject.com/en/dev/ref/models/fields/#foreignkey>`
field, except for a subtle difference: it supports `othermodel` being
`None` or the name of some non-installed model and returns a
:class:`DummyField` in that case.  This difference is useful when
designing reusable models.

.. class:: CustomField

Mixin to create a custom field. It defines a single method
:meth:`dd.CustomField.create_layout_elem`


  .. method:: create_layout_elem(self, layout_handle, field, **kw)

     Instantiate and return some subclass of
     :class:`lino.ui.elems.LayoutElement` to be used in
     `layout_handle`.

     `self` and `field` are identical unless self is a RemoteField or
     a :class:`dd.VirtualField`.


.. class:: VirtualField

Represents a virtual field. Virtual fields are not stored in the
database, but computed each time they are read. Django doesn't see
them.


.. function:: is_abstract_model(name)

  Return True if the named model is declared as being extended by
  :attr:`ad.Plugin.extends_models`.

  `name` must be a string with the full model name, e.g. ``"myapp.MyModel"``.


.. function:: is_hidden_app(app_label)

  Return True if the app is known, but has been disabled using 
  :meth:`ad.Site.get_apps_modifiers`.


.. function:: login(self, username=None, **kw)

    For usage from a shell.

    The :meth:`login <lino.site.Site.login>` method doesn't require any
    password because when somebody has command-line access we trust
    that she has already authenticated. It returns a
    :class:`BaseRequest <lino.core.requests.BaseRequest>` object which
    has a :meth:`show <lino.core.requests.BaseRequest.show>` method.

.. function:: startup()

Start up this Site. 

This is called exactly once when Django has has populated it's model
cache.

It is designed to be called potentially several times in case your
code wants to make sure that it was called.


.. function:: get_db_overview_rst

.. function:: is_installed(app_label)

    Return `True` if :setting:`INSTALLED_APPS` contains an item
    which ends with the specified `app_label`.

.. function:: on_each_app(self, methname, *args)

    Call the named method on the :xfile:`models.py` module of each
    installed app.

.. function:: for_each_app(self, func, *args, **kw)
 
    Successor of :func:`dd.on_each_app`.  This also loops over

    - apps that don't have a models module
    - inherited apps

.. attribute:: plugins

    Alias for :attr:`apps` for backward compatibility.

.. attribute:: apps

    An :class:`AttrDict` object with one entry for each installed app,
    mapping to the :class:`ad.Plugin` of that app.

.. attribute:: logger

    Shortcut to the Lino logger.


.. function:: makedirs_if_missing(dirname)

    Make missing directories if they don't exist
    and if :attr:`ad.Site.make_missing_dirs` is `True`.



