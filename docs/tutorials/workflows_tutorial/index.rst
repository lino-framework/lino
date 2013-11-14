.. _lino.tutorial.workflows:

Workflows
---------

This tutorial explains how to use workflows.
It extends the application created in :ref:`lino.tutorial.watch`,
so you should do that tutorial before reading on here.

Vocabulary: in Lino a "workflow" is a combination of
(1) a list of possible "states" (aka "life cycle") and
(2) a list of "transitions", i.e. actions which change from one state 
to another state.


We recommend to define workflows in a separate module 
(to make them reusable or even exchangeable, but that's worth another 
tutorial), 
here it is called simply `workflows.py`:

.. literalinclude:: workflows.py

In `models.py` there are only a few changes (compared to :ref:`lino.tutorial.watch`), 
first we need import the `EntryStates` workflow, and then change the 
Entry model to use it::

    from .workflows import EntryStates
    ...
    class Entry(dd.CreatedModified,dd.UserAuthored):
        workflow_state_field = 'state'
        ...
        state = EntryStates.field()
        

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
    
    
    


Questions and answers
---------------------

**Is there a possibility to decide if the transition is available in runtime?**

Yes, the :meth:`get_action_permission 
<lino.core.actions.Action.get_action_permission>` 
method, as used by the ``StartEntry`` action in our example. 
It is called once for every record and thus should not take too much energy.
In the example application, you can see that the "Start" action is *not* shown 
for entries with one of the company, subject or body fields empty.
Follow the link to the API reference for details.

Note that if you test only the profile of the requesting user, 
or some value from ``settings``, then you'll rather define a 
:meth:`get_view_permission 
<lino.core.actions.Action.get_view_permission>` 
method. That's more effivient because it is called only once for every 
user profile at server startup.


**Why do I  have to declare ``workflow_state_field``?**

This and the third parameter "state" indeed seem useless at the moment. 
It is because we are thinking of allowing more than one state 
field per model. i.e. a kind of parallel life cycles.
I am myself not yet sure whether this would be a great feature 
or a mousetrap.

