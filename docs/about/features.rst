=========================
Features and design goals
=========================
    
Design goals
------------

- Lino applications are intuitive and easy-to-understand for the end user.
  (see :doc:`values`)
- sustainable application development
- agile programming
- rapid prototyping 
- libraries of reusable code
- short release cycles
- maintainable code
- stable 

.. _lino.features:

Features
--------

Because Lino applications are Django projects, the following features
(copied from the `Django website <https://www.djangoproject.com/>`_)
also apply to Lino:

- **Object-relational mapper** :
  Define your data models entirely in Python. 
  You get a rich, dynamic database-access API for free -- 
  but you can still write SQL if needed.
  
- **Internationalization** :
  Django has full support for multi-language applications, 
  letting you specify translation strings and providing 
  hooks for language-specific functionality.  

- **Cache system** :
  Hook into memcached or other cache frameworks for super performance 
  -- caching is as granular as you need.
  
Lino then adds its own features to the above:

- An out-of-the-box :doc:`user interface </topics/ui>`.  Lino
  application developers don't waste their time writing html templates
  or css.

- :ref:`Layouts <layouts>`:
  use the Python language not only
  for designing your *models* but also your *forms*.
  
- Lino adds enterprise-level concepts for definining 
  :ref:`permissions` and :ref:`workflows`.
  
- :ref:`mldbc` : 
  Use Lino's rich experience with applications that manage 
  multilingual database content.
  
- Use Lino's tools for generating :ref:`userdocs`.
  
- Lino includes :ref:`dpy`, a great alternative to `Django's built-in
  migration system
  <https://docs.djangoproject.com/en/dev/topics/migrations/>`_ to
  manage your :ref:`database migrations <datamig>`.
  
- Other features include extensions to handle :ref:`polymorphism`.
  
- And last but not least, Lino includes :mod:`lino_modlib`, a
  collection of reusable Django apps designed for Lino applications.


.. _lino.think_python:

Think Python
------------

When using Lino, you should understand a fundamental design choice of
the Lino framework:

We believe that database structure, screen layouts and business logic
should be written in *Python*, not in *XML*. That is, they should be
done by the programmer, not by the end-users.

Python is a powerful and well-known parser, why should we throw away a
subset of its features by introducing yet another textual description
language?  The main reason why other frameworks do this is that it
enables them to have non-programmers do the database design and screen
layouts. Which is a pseudo-advantage.

Lino is here because we believe that database design and screen layout
should *not* be delegated to people who don't *think in Python*.

This does not explude usage of templates when meaningful. 

A missing piece here are features like user-defined views
(:ticket:`848`) because end-users of course sometimes want (and should
have a possibility) to save a given grid layout.


