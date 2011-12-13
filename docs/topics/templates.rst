Templates
=========

While the details on how to call Python code from a template 
depends on the build method you use, there are some general 
things to know for all cases where a system administrator 
uses Lino's Python code.


Person
------

(You can ignore the following lines of Python code; 
they are here because this article is being tested automatically)

>>> from lino.tools import resolve_model
>>> Person = resolve_model('contacts.Person')
>>> person = Person.objects.get(pk=117)

The property "full_name" (without parentheses) of Person 
is an alias for the function call `get_full_name()` without parameters.

>>> person.full_name
Herrn Andreas ARENS

>>> person.get_full_name()
Herrn Andreas ARENS

The :func:`get_full_name <lino.modlib.contacts.models.Person.get_full_name>` 
function has 2 optional parameters `nominative` and `salutation`:

>>> person.get_full_name(nominative=True)
Herr Andreas ARENS

>>> person.get_full_name(salutation=False)
Andreas ARENS

You can also get the components of the full name separately:

>>> person.get_salutation(nominative=True)
Herr
>>> person.first_name
Andreas
>>> person.last_name
Arens
