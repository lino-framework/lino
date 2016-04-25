=================
Developer's Guide
=================

This is the central meeting place for Lino application developers.  We
are doing our best to grow this into a pedagogically meaningful
sequence of articles.

Getting started
===============


.. toctree::
   :maxdepth: 1
   :hidden:

   install
   /tutorials/polls/mysite/index
   /tutorials/hello/index
   /tutorials/dumpy
   /tutorials/tables/index
   layouts
   /tutorials/lets/index

#.  :doc:`/dev/install` : How to install Lino. System requirements. "Released
    version" versus "Development version". How to run Lino's test
    suite.

#.  :doc:`/tutorials/polls/mysite/index` : In this section we are
    going to convert the “Polls” application from Django’s tutorial
    into a Lino application. This will illustrate some differences
    between Lino and Django.

#.  :doc:`/tutorials/hello/index` : The first Lino application running
    on your machine. It's easier than with Django. A ``settings.py`` and
    a ``manage.py``. Initialize a demo database. Run a development
    server.

#.  :doc:`/tutorials/dumpy` : The ``initdb`` and ``initdb_demo``
    commands.  Playing with fixtures.  Writing your own fixture.

#.  :doc:`/tutorials/tables/index` : Models, tables and views. What is a
    table? Designing your tables. Using tables without a web server.

#.  :doc:`layouts` : About layouts, detail windows, data elements and
    panels.

#.  :doc:`/tutorials/lets/index` : A full-stack example about the work
    of a Lino application developer.  Writing a technical specification.
    Describing a database structure. Designing your tables. Writing demo
    data. Writing test cases. Menu structure and main page. Form
    layouts.


Getting acquaintained
=====================

#.  :doc:`settings` : The Django settings module. How Lino integrates
    into Django settings. Inheriting settings.
#.  :doc:`application` : An app is not an application.
#.  :doc:`plugins` : Why we need plugins. Configuring plugins.
#.  :doc:`users` : Why do we replace Django's user management. Passwords.
#.  :doc:`site` : Instantiating a `Site`.  Specifying the
    `INSTALLED_APPS`. Additional local apps.
#.  :doc:`dump2py` : Python dumps
#.  :doc:`site_config` : The SiteConfig used to store "global" site-wide
    parameters in the database.
#.  :doc:`languages` : if you write applications for users who don't
    speak English.
#.  :doc:`i18n` : About "internationalization" and "translatable strings".
#.  :doc:`menu` : Standard items of a main menu
#.  :doc:`actors` :
#.  :doc:`choicelists` :
#.  :doc:`parameters` :
#.  :doc:`virtualfields` :
#.  :doc:`ar` : Using action requests
#.  :doc:`html` : Generating HTML
#.  :doc:`custom_actions` : Writing custom actions
#.  :doc:`action_parameters` :
#.  :doc:`gfks` : Lino and `GenericForeignKey` fields

#.  :doc:`/tutorials/letsmti/index` :
#.  :doc:`/tutorials/layouts` :
#.  :doc:`/tutorials/vtables/index` :
#.  :doc:`actions` :
#.  :doc:`/tutorials/actions/index` :
#.  :doc:`/tutorials/mldbc/index` :
#.  :doc:`/tutorials/human/index` :
#.  :doc:`plugin_inheritance` : Plugin inheritance
#.  :doc:`plugin_cooperation` : Plugin cooperation
#.  :doc:`printing` : (TODO)
#.  :doc:`cache` : telling Lino where to store temporari files.
#.  :doc:`rendering` : 

.. toctree::
   :maxdepth: 1
   :hidden:

   settings
   application
   plugins
   site
   dump2py
   site_config
   users
   languages
   i18n
   menu
   actors
   choicelists
   parameters
   ar
   virtualfields
   html
   custom_actions
   action_parameters
   gfks
   /tutorials/letsmti/index
   /tutorials/layouts
   /tutorials/vtables/index
   actions
   /tutorials/actions/index
   /tutorials/mldbc/index
   /tutorials/human/index
   plugin_inheritance
   plugin_cooperation
   printing
   cache
   rendering
   

Special topics
==============

.. toctree::
   :maxdepth: 1

   /tutorials/addrloc/index
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
   /tutorials/gfktest/index
   /tutorials/belref/index

   setup

Drafts
======
   
.. toctree::
   :maxdepth: 1

   /tutorials/tested_docs/index
   startup
   perms
   /tutorials/myroles/index
   workflows
   pull
   translate/index

   testing
   
   help_texts
   userdocs
   signals
   intro
   style
   datamig
   versioning
   versions
   extjs


Other
-----

.. toctree::
   :maxdepth: 1

   /changes
   /todo
   /tested/index
   git
   /ref/index
   py3



.. toctree::
   :hidden:

   tables
   fields
   ad
   dd
   rt
   mixins
   /tutorials/index
   ml/index
   
