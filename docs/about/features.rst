=====================================
Features, design goals  & limitations
=====================================
    
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

- :ref:`layouts`:
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
  
- And last but not least, Lino includes :mod:`ml`, a collection of
  reusable Django apps designed for Lino applications.


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


Limitations
-----------

- Lino does not even *try* to be very easy to learn. There are other
  frameworks who try to deliver quick visible results. With Lino it
  may take a day or two before you fall in love with it, but your love
  will last longer.

- Lino has no "visual GUI editor" because one of it's powerful
  features are :ref:`layouts` whose purpose is to describe user
  interfaces programmatically in the Python language.  We don't
  believe that a visual GUI editor is a good thing when it comes to
  maintaining complex database applications in a sustainable way. Rob
  Galanakis explains a similar opinion in `GeoCities and the Qt
  Designer
  <http://www.robg3d.com/2014/08/geocities-and-the-qt-designer/>`_

- Lino is not well documented. This is a disadvantage of using a young
  framework with a small community. But we are working on it. Give
  your feedback, tell us where you got stuck, help us to grow!



