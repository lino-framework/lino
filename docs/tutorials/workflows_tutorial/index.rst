.. _lino.tutorial.workflows:

Workflows
---------

This tutorial explains how to 
use workflows.
It extends the application created in :ref:`lino.tutorial.watch`,
so you should do that tutorial before reading on here.

.. literalinclude:: workflows.py

In models.py there are only a few changes, 
first we need import `EntryStates`::

  from .workflows import EntryStates
  
And then we must change the Entry model to use it::

    class Entry(dd.CreatedModified,dd.UserAuthored):
        workflow_state_field = 'state'
        ...
        state = EntryStates.field()
        
Note: currently you have to declare `workflow_state_field` for 
historical reasons.

And finally we added the `workflow_buttons` at different places: 
in the detail layout of Entry, and in a `column_names` attribute to 
`EntriesByCompany` and `MyEntries`. 
That's because `workflow_buttons` 
is a virtual field and therefore not automatically included.


You can play with this application by cloning the latest development 
version of Lino, then ``cd`` to the :file:`/docs/tutorials/workflow_tutorial` 
directory where you can run::

    $ python manage.py initdb_demo
    $ mkdir media 
    $ python manage.py runserver

