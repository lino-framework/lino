.. _dev.actions: 

=======
Actions
=======

Note: this is intended to be a rather dry but complete document for
reference purposes.  See also some tutorials:

- :doc:`/tutorials/actions/index`


Overview
--------

Lino has a unique API for writing custom actions in your application.

.. set_response:

The ``set_response()`` method
-----------------------------

The :meth:`set_response <lino.core.requests.BaseRequest.set_response>`
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
