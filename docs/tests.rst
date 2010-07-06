Tests
=====

Using the ``.. graphviz::`` directive:

.. graphviz::

   digraph foo {
      "bar" -> "baz";
   }
   
   
   
Using the ``.. inheritance-diagram::`` directive:

.. inheritance-diagram:: 
  lino.modlib.contacts.models.Contact  dsbe.models.Contact
  lino.modlib.contacts.models.Person   dsbe.models.Person
  lino.modlib.contacts.models.Company  dsbe.models.Company



Modules
-------

See also :doc:`rfc/P20100706` 

.. automodule:: lino
  :members:
  :undoc-members:

.. automodule:: lino.reports

.. automodule:: lino.ui.extjsu

.. automodule:: lino.ui.extjsw

.. automodule:: lino.modlib.fields


