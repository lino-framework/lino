===============================
How to write user documentation
===============================


Lino includes a set of tools for writing comprehensive 
multi-lingual user documentation for your Lino application.
It is a combination of `Django <https://docs.djangoproject.com>`_'s 
and `Sphinx <http://sphinx-doc.org/>`_'s strength's.

When developing and maintaining a Lino application we suggest to
use two distinct Sphinx document trees:

- `/docs` for technical documentation (only English) 
- `/userdocs` for user documentation (translated)

See also the :ref:`atelier.sphinxext` documentation page 
of :ref:`atelier`.


.. rst:role:: ddref

Insert a reference to the user documentation of an item of the data
dictionary of the Lino Site associated to this doctree.

This role is available only when this project has a userdocs.

.. rst:directive:: actor

Generate and insert user documentation for the specified actor.
If this directive has content, this will be inserted at the beginning.






