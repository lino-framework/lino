.. _noi.guide:

=====================
Lino Noi User's Guide
=====================

A little crash course:

- Point your browser to http://team.lino-framework.org/
  and log in as user *jean*.

- Open the list of all tickets using the quicklink "[Tickets]" or the
  menu :menuselection:`Tickets--> Tickets`

.. image:: 1.png

- Click the :guilabel:`Insert` button to create a new ticket:

  - Reporter: (you)
  - Product: (leave empty)
  - Summary: "Getting started with Lino Noi"

  Click the :guilabel:`Create` button or press :kbd:`ENTER` to confirm
  the insert window.

Beware the pitfall: After creating the ticket, click the "Save" button
once (or type Ctrl-S) in order to avoid #219 ("Lino sends second POST
when clicking StartSession on newly created record"). Sorry for this bug.

When you create a ticket, Lino automatically also creates a new
session on that ticket which starts at current time.  (If it doesn't,
then go to your user preferences and check the :guilabel:`Open session
on new ticket` checkbox).

.. image:: 1.png

Your session is visible as a row in the lower right table
"Sessions". You should write at least a few words in the "Summary" of
your session (by pressing :kbd:`F2` on that field). Now you are
supposed to work on that ticket. When you stopped working, click the
:guilabel:`↘` link in the :guilabel:`Workflow` field of the
ticket. Lino will fill the :guilabel:`End time` field of your session
with the current time.

You can manually change the start and end times by pressing :kbd:`F2`
on these field.

Now klick on the :guilabel:`↗` in the :guilabel:`Workflow` field of
the ticket. This will create a new session which starts at current
time.  Note that the :guilabel:`↗` in the :guilabel:`Workflow` field
has changed to a :guilabel:`↘`. That's because the ticket has a
started session with an empty :guilabel:`End time`.

Note another little oddness: you can manually clear the "End time"
field of your session, but for the moment you must then manually click
:guilabel:`Refresh` button of your ticket so that Lino replaces the
:guilabel:`↘` by a :guilabel:`↗`.

Using this system, you can see your exact hours worked. 

This is how a typical week looks for me. I can click on the link of a
date (in first column) to see (and possibly edit) all sessions of that
day. When I hover the mouse over a ticket number, it shows the
ticket's summary.

