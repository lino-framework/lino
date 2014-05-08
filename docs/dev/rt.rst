===========
Runtime API
===========

This section documents classes which are important at runtime.

.. currentmodule:: rt


The ``ActionRequest`` class
---------------------------

.. class:: ActionRequest

    An action request is when a given user asks to run a given action
    of a given actor.

    Every Django web request is wrapped into an action request.

    But an ActionRequest also holds extended information about the
    "context" (like the "renderer" being used) and provides the
    application with methods to communicate with the user.

    A bare BaseRequest instance is returned as a "session" by
    :meth:`login <lino.site.Site.login>`.



  .. method:: show(self, spec, master_instance=None,
              column_names=None, header_level=None, 
              language=None, **kw)

    Show the table specified by `spec` according to the current
    renderer.  If the table is a :term:`slave table`, then a
    `master_instance` must be specified as second argument.

    Optional keyword arguments are

    - `column_names` overrides default list of columns
    - `header_level` show also the header (using specified level)
    - `language` overrides the default language used for headers and
      translatable data

    Usage in a tested doc::

      >>> ses = settings.SITE.login("robin")
      >>> ses.show('users.UsersOverview')

    Usage in a Jinja template::

      {{ar.show('users.UsersOverview')}}

    Usage in an appy.pod template::

      do text from ar.show('users.UsersOverview')

    Note that this function either returns a string or prints to
    stdout and returns None, depending on the current renderer.


  .. method:: set_response()

    The :meth:`set_response`
    method of an action request is used to communicate with the user.


    This does not yet respond anything, it is stored until the
    action has finished. The response might be overwritten by
    subsequent calls to `set_response`.

    Allowed keywords are:

    - ``message`` -- a string with a message to be shown to the user.

    - ``alert`` -- True to specify that the message is rather important
      and should alert and should be presented in a dialog box to be
      confirmed by the user.

    - ``success``
    - ``errors``
    - ``html``
    - ``rows``
    - ``data_record``
    - ``goto_record_id``
    - ``refresh``
    - ``refresh_all``
    - ``close_window``
    - ``xcallback``
    - ``open_url``
    - ``open_davlink_url``
    - ``info_message``
    - ``warning_message``
    - ``eval_js``

  .. method:: table2xhtml(self, header_level=None, **kw)
     
    Available only when the actor is a :class:`dd.AbstractTable`.

  .. method:: dump2html(self, tble, data_iterator, column_names=None):

    Available only when the actor is a :class:`dd.AbstractTable`.

    Render this table into an existing
    :class:`lino.utils.xmlgen.html.Table` instance.

  .. method:: get_field_info(ar, column_names=None)

    Return a tuple (fields, headers, widths) which expresses which
    columns, headers and widths the user wants for this request. If
    `self` has web request info, checks for GET parameters cn, cw and
    ch (coming from the grid widget). Also apply the tables's
    :meth:`override_column_headers
    <dd.Actor.override_column_headers>` method.



