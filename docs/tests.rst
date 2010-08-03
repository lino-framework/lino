Tests
=====


Using the ``.. graphviz::`` directive
-------------------------------------

.. graphviz::

   digraph foo {
      "bar" -> "baz";
   }
   
   

Using the ``.. inheritance-diagram::`` directive
------------------------------------------------

::

  .. inheritance-diagram:: 
    lino.modlib.contacts.models.Contact  dsbe.models.Contact
    lino.modlib.contacts.models.Person   dsbe.models.Person
    lino.modlib.contacts.models.Company  dsbe.models.Company



