.. _application:

===============================
What is a software application?
===============================


    "In information technology, an application is a computer program
    designed to help people perform an activity."
    -- `Wikipedia <http://en.wikipedia.org/wiki/Software_application>`_

    A software application is a piece of software which is perceived
    as an entity by end-users.
    -- Luc Saffre



.. currentmodule:: ad

An application is not an app
----------------------------

Django comes with a rather special use of the word "app".  Daniel and
Audrey (`Two scoops of Django <https://django.2scoops.org/>`_) say it
in a diplomatic way:

  "It's not uncommon for new Django developers to become understandably 
  confused by Django's usage of the word 'app'."

If you ask me: Django is simply wrong here.  Django says "app" where
it should say "plugin".  An application is a standalone piece of
software.  `django.contrib.contenttypes` is not what everybody (except
Django people) would call an application, it is a **plugin**.

But okay, that's basically just a vocabulary problem.  Many Django
people are more or less aware of that problem, but it would be really
much work to fix it because the word is used in variables like
`app_label` and :setting:`INSTALLED_APPS`.  Too much work for "just a
vocabulary" problem.  We have to live with it and forgive Django its
oddness.

We suggest to differentiate between "app" and "application".  We can
continue to call them "apps", but should refrain from expanding that
word to "application". Because apps are *not* applications, they are
plugins which we happen to call "app" for historical reasons.  This
rule shouldn't offend even the most conservative Django developer.

The problem with this "vocabulary" problem is that it leaves us (Lino
developers) with no word left for what we would call an application.
A Lino application is neither an "app" nor a "project".  That's why we
decided to speak about a :class:`Site` class and a :setting:`SITE`
setting rather than an ``Application`` class and an ``APP`` setting.


So what then is an application really?
======================================

The :class:`Site` is the base clase for representing a "Lino
application".  It has attributes like :attr:`Site.verbose_name` (the
"short" user-visible name) and the :attr:`Site.version` which are used
by the method :meth:`Site.welcome_text`.  It also defines a
:meth:`Site.startup` method and signals, which is the concrete reason
why you might want a bare :class:`Site`.

But then it is designed to be subclassed.  It is subclassed by
:class:`north.Site`, which is subclassed by :class:`lino.Site`, then
subclassed by the application developer
(e.g. :class:`lino.projects.min1.settings.Site`), then imported into a
local :xfile:`settings.py`, where the system administrator may
subclass it another time before finally instantiating it, and
assigning it to the :setting:`SITE` variable.

Such a Site instance would then be a "project" for Django.

This brings an additional level of encapsulation to Django.  A `Site`
is a kind of "master app" or "project template".  A Site is a
"collection of apps" which make up a whole.

A Site is usually meant to work for a given set of Django apps.  There
are different mechanisms to define "automatic" ways of building the
content of :setting:`INSTALLED_APPS` setting.  (TODO: write more about
it)


