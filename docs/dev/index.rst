=================
Developer's Guide
=================

This is the central meeting place for Lino application developers.  We
are doing our best to grow this into a pedagogically meaningful
sequence of articles.

.. include:: /include/wip.rst

Getting started
===============


.. toctree::
   :maxdepth: 1
   :hidden:

   install
   /tutorials/hello/index
   /tutorials/polls/mysite/index
   /tutorials/dumpy
   /tutorials/tables/index
   /tutorials/lets/index

- :doc:`/dev/install` : How to install Lino. System requirements. "Released
  version" versus "Development version". How to run Lino's test
  suite.

- :doc:`/tutorials/hello/index` : The first Lino application running
  on your machine. It's easier than with Django. A ``settings.py`` and
  a ``manage.py``. Initialize a demo database. Run a development
  server.

- :doc:`/tutorials/polls/mysite/index` : We convert the “Polls”
  application from Django’s tutorial into a Lino application. This
  will introduce some differences between Lino and Django.

- :doc:`/tutorials/dumpy` : The ``initdb`` and ``initdb_demo``
  commands.  Playing with fixtures.  Writing your own fixture.

- :doc:`/tutorials/tables/index` : Models, tables and views. What is a
  table? Designing your tables. Using tables without a web server.

- :doc:`/tutorials/lets/index` : What is a technical specification?
  Describing a database structure. Designing your tables. Writing demo
  data. Writing test cases. Menu structure and main page. Form layouts.


Getting acquaintained
=====================

-  :doc:`application` : An app is not an application. Introducing the :class:`Site` class.
-  :doc:`menu` :
-  :doc:`choicelists` :
-  :doc:`actors` :
-  :doc:`/tutorials/letsmti/index` :
-  :doc:`/tutorials/layouts` :
-  :doc:`/tutorials/vtables/index` :
-  :doc:`actions` :
-  :doc:`/tutorials/actions/index` :
-  :doc:`/tutorials/mldbc/index` :
-  :doc:`/tutorials/human/index` :

.. toctree::
   :maxdepth: 1
   :hidden:

   application
   menu
   choicelists
   actors
   /tutorials/letsmti/index
   /tutorials/layouts
   /tutorials/vtables/index
   actions
   /tutorials/actions/index
   /tutorials/mldbc/index
   /tutorials/human/index
   

Reference
=========

.. toctree::
   :maxdepth: 1

   layouts

   ml/index
   

Special topics
==============

.. toctree::
   :maxdepth: 1

   /tutorials/mti/index
   /tutorials/sendchanges/index
   /tutorials/actors/index
   /tutorials/de_BE/index
   /tutorials/watch_tutorial/index
   /tutorials/workflows_tutorial/index
   /tutorials/matrix_tutorial/index

   /tutorials/auto_create/index
   /tutorials/pisa/index
   /tutorials/input_mask/index


Drafts
======
   
.. toctree::
   :maxdepth: 1

   /tutorials/tested_docs/index
   settings
   startup
   perms
   workflows
   pull
   translate/index

   apps
   testing
   
   help_texts
   userdocs
   signals
   intro
   style
   datamig
   versioning
   users


Other
-----

.. toctree::
   :maxdepth: 1

   /changes
   /todo
   /tested/index
   git
   /ref/index



.. toctree::
   :hidden:

   tables
   fields
   ad
   dd
   rt
   mixins
