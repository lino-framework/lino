=============
The menu tree
=============

As we have seen, a description of a database application contains
models, tables and layouts.  Another important part are custom actions
(coming soon).  But one important piece is missing: the **main menu**.

The main menu defines how the different functionalities of an
application should be presented to the user.

The application developer must decide 

organize the different actors and
actions of her application into a "menu structure".

This menu structure defines another level of grouping (into menu
groups).

Standard items of a main menu
=============================

:meth:`lino.core.site.Site.setup_menu`
:attr:`lino.core.site.Site.top_level_menus`


The Main menu
-------------

setup_main_menu

.. _config_menu:

The Configuration menu
----------------------

setup_config_menu

The Explorer menu
-----------------

setup_explorer_menu
 
.. _menu.groups:


Introduction to menu groups
===========================

The different installed apps (identified by their `app_label`) are one
way to group your database models into different "modules".  But this
grouping almost never exactly matches how the users would modularize
their application.


TODO: write more about it.


