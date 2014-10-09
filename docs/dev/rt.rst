====================
Runtime API (``rt``)
====================

This section documents functions and classes which are available "at
runtime", i.e. when the Django machine has been initialized.

You may *import* it at the global namespace of a :xfile:`models.py`
file, but you should use it only when the :func:`startup` function has
been called.


.. currentmodule:: rt

.. function:: startup()

Start up this Site. 

This is called exactly once when Django has has populated it's model
cache.

It is designed to be called potentially several times in case your
code wants to make sure that it was called.

.. data:: modules

An :class:`atelier.utils.AttrDict` with one entry per `app_label`,
each entry holding a reference to each actor of that app.


.. function:: login(self, username=None, **kw)

    For usage from a shell.

    The :meth:`rt.login` method doesn't require any
    password because when somebody has command-line access we trust
    that she has already authenticated. It returns a
    :class:`BaseRequest <rt.BaseRequest>` object which
    has a :meth:`rt.show <lino.core.requests.BaseRequest.show>` method.

.. function:: show

  Calls :meth:`ar.show` on a temporary anonymous session (created
  using :meth:`Site.login`).


Using the ``ConfigDirCache``
----------------------------

.. function:: find_config_file(filename, *groups)

    Return the full path of the first occurence within the
    :class:`lino.utils.config.ConfigDirCache` of a file named
    `filename`

.. function:: find_config_files(pattern, *groups)

    Returns a dict of `filename` -> `config_dir` entries for each config
    file on this site that matches the pattern.  Loops through
    `config_dirs` and collects matching files.  When a filename is
    provided by more than one app, then the latest app gets it.

    `groups` is a tuple of strings, e.g. '', 'foo', 'foo/bar', ...


.. function:: find_template_config_files(template_ext, *groups)

    Like :func:`find_config_files`, but ignore babel variants:
    e.g. ignore "foo_fr.html" if "foo.html" exists.
    Note: but don't ignore "my_template.html"

Action requests
---------------

.. class:: ar

    An action request is when a given user asks to run a given action
    of a given actor.  

    As a rough approcimation you can say that every Django web request
    gets wrapped into an action request.  The ActionRequest just holds
    extended information about the "context" (like the "renderer"
    being used) and provides the application with methods to
    communicate with the user.
    But there are exceptions, the :attr:`ar.request` can be None.

    Implemented by :class:`lino.core.requests.BaseRequest` and its
    subclasses.

  .. method:: show(self, spec, master_instance=None, column_names=None, header_level=None, language=None, **kw)

    Show the specified table or action using the current renderer.  If
    the table is a :term:`slave table`, then a `master_instance` must
    be specified as second argument.

    The first argument, `spec` can be:
    - a string with the name of a model, actor or action
    - another action request
    - a bound action (i.e. a :class:`BoundAction` instance)

    Optional keyword arguments are

    - `column_names` overrides default list of columns
    - `header_level` show also the header (using specified level)
    - `language` overrides the default language used for headers and
      translatable data

    Any other keyword arguments are forwarded to :meth:`spawn`.

    Usage in a tested doc::

      >>> rt.login('robin').show('users.UsersOverview', limit=5)

    Usage in a Jinja template::

      {{ar.show('users.UsersOverview')}}

    Usage in an appy.pod template::

      do text from ar.show('users.UsersOverview')

    Note that this function either returns a string or prints to
    stdout and returns None, depending on the current renderer.


  .. method:: spawn(spec, **kwargs)

    Create a new ActionRequest using default values from this one and
    the action specified by `spec`.  

  .. method:: success()

    Tell client to consider the action as successful. This is the same as
    :meth:`set_response` with `success=True`.

  .. method:: close_window()

    Ask client to close the current window. This is the same as
    :meth:`set_response` with `close_window=True`.

  .. method:: set_response(**kw)

    Set (some part of) the response to be sent when the action request
    finishes.  
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

    This does not yet respond anything, it is stored until the action
    has finished. The response might be overwritten by subsequent
    calls to :meth:`set_response`.

    :js:func:`Lino.handle_action_result` will get these instructions
    as *keywords* and thus will not know the order in which they have
    been issued. This is a design decision.  We *want* that, when
    writing custom actions, the order of these instructions does not
    matter.

  .. method:: add_system_note(self, owner, subject, body, silent)

    Send a system note with given `subject` and `body` and attached to
    database object `owner`.

    A system note is a text message attached to a given database
    object instance (`owner`) and propagated through a series of
    customizable and configurable channels.

    The text part consists basically of a subject and a body, both
    usually generated by the application and edited by the user in
    an action's parameters dialog box.

    This method will build the list of email recipients by calling the
    global :meth:`ad.Site.get_system_note_recipients` method and send
    an email to each of these recipients.

  .. method:: table2xhtml(self, header_level=None, **kw)
     
    Available only when the actor is a :class:`dd.AbstractTable`.

  .. method:: dump2html(self, tble, data_iterator, column_names=None):

    Available only when the actor is a :class:`dd.AbstractTable`.

    Render this table into an existing
    :class:`lino.utils.xmlgen.html.Table` instance.

  .. method:: goto_instance(self, obj, **kw)

    Ask the client to display a :term:`detail window` on the given
    record. The client might ignore this if Lino does not know a
    detail window.

    This is a utility wrapper around :meth:`set_response` which sets
    either `data_record` or a `record_id`.

    Usually `data_record`, except if it is a `file upload
    <https://docs.djangoproject.com/en/dev/topics/http/file-uploads/>`_
    where some mysterious decoding problems (:blogref:`20120209`)
    force us to return a `record_id` which has the same visible
    result but using an additional GET.

    If the calling window is a detail on the same table, then it
    should simply get updated to the given record. Otherwise open a
    new detail window.

  .. method:: get_field_info(self, ar, column_names=None)

    Return a tuple (fields, headers, widths) which expresses which
    columns, headers and widths the user wants for this request. If
    `self` has web request info, checks for GET parameters cn, cw and
    ch (coming from the grid widget). Also apply the tables's
    :meth:`override_column_headers
    <dd.Actor.override_column_headers>` method.


  .. method:: insert_button(self, text=None, known_values={}, **options)

    Returns the HTML of an action link which will open the
    :term:`insert window` of this request.

  .. method:: action_button(self, ba, obj, *args, **kw)

    Returns the HTML of an action link which will run the specified
    action.

    ``kw`` may contain additional html attributes like `style`.


  .. method:: parse_req(self, request, rqdata, **kw):

    Parse the given Django request and setup from it.

  .. attribute:: request

    The Django request objects which caused this action request.

  .. method:: get_help_url(docname=None, text=None, **kw)

    Generate a link to the help section of the documentation (whose
    base is defined by :attr:`ad.Site.help_url`)

    Usage example::

        help = ar.get_help_url("foo", target='_blank')
        msg = _("You have a problem with foo."
                "Please consult %(help)s "
                "or ask your system administrator.")
        msg %= dict(help=E.tostring(help))
        kw.update(message=msg, alert=True)

    The :ref:`lino.tutorial.pisa` tutorial shows a resulting message
    generated by the print action.
