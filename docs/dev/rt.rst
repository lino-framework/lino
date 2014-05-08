===========
Runtime API
===========

This section documents classes which are important at runtime.

.. currentmodule:: rt


The ``ActionRequest`` class reference
-------------------------------------

.. class:: rt.ActionRequest


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

.. class:: rt.TableRequest

  Represents an :class:`ActionRequest` on a :class:`table
  <dd.AbstractTable>`.

  .. method:: table2xhtml(self, header_level=None, **kw)

  .. method:: dump2html(self, tble, data_iterator, column_names=None):

    Render this TableRequest into an existing
    :class:`lino.utils.xmlgen.html.Table` instance.

  .. method:: get_field_info(ar, column_names=None)

    Return a tuple (fields, headers, widths) which expresses which
    columns, headers and widths the user wants for this
    TableRequest. If `self` has web request info, checks for GET
    parameters cn, cw and ch (coming from the grid widget). Also
    apply the tables's :meth:`override_column_headers
    <lino.core.actors.Actor.override_column_headers>` method.

