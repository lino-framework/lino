========================
Database Design (``dd``)
========================

.. module:: dd

The :mod:`lino.dd` module is a shortcut to those parts of Lino which
are used in your :xfile:`models.py` modules.  The name ``dd`` stands
for "Database Design".

.. toctree::
   :maxdepth: 2

   actors
   mixins
   fields
   layouts
   actions



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

.. function:: is_abstract_model(name)

  Return True if the named model is declared as being extended by
  :attr:`ad.Plugin.extends_models`.

  `name` must be a string with the full model name, e.g. ``"myapp.MyModel"``.


.. function:: is_hidden_app(app_label)

  Return True if the app is known, but has been disabled using 
  :meth:`ad.Site.get_apps_modifiers`.


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

