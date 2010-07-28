======
Models
======

Django identifies models and SQL tables using a string of format `app_label.model_name`. 
The app_label is usually added automatically by taking the second-last 
part of the full Python module name. For example if you define two classes
`foo.sales.models.Invoice` and `bar.sales.models.Invoice` 
(both subclasses of django.db.models.Model) and install them both 
using ``INSTALLED_APPS = ['foo.sales', 'bar.sales']``, then one of them will 
override the other.

Lino uses this behaviour to allow creating reusable Reports and Menus that 
are not limited to a known implementation of a model will be used.

That's why we need a convention of *common model names* and what they are used for.


contacts.Company
----------------

.. model:: contacts.Company
.. report:: contacts.Companies

  Used to store organisations of any kind. Also non-formal groups of persons.
  
contacts.Person
---------------

.. model:: contacts.Person
.. report:: contacts.Persons

  Used to store physical persons.
  
countries.Country
-----------------

.. model:: countries.Country
.. report:: countries.Countries

  