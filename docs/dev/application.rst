.. _application:

==================
The ``Site`` class
==================

.. currentmodule:: lino.core.site_def

One of the important things to understand when you learn Lino is the
:class:`Site` class.  

But first we need to tidy up your brain:

An app is not an application
============================

A **software application** is a standalone piece of software which is
perceived as an entity by end-users.

    In information technology, an application is a computer program
    designed to help people perform an activity.
    -- `Wikipedia <http://en.wikipedia.org/wiki/Software_application>`_

Unfortunately, Django comes with a rather special use of the word
"app".  Daniel and Audrey (`Two scoops of Django
<https://django.2scoops.org/>`_) say it in a diplomatic way: "It's not
uncommon for new Django developers to become understandably confused
by Django's usage of the word 'app'."

And if you ask me: Django is simply wrong here.  Django says "app"
where it should say "plugin". Things like `django.contrib.contenttypes
<https://docs.djangoproject.com/en/1.7/ref/contrib/contenttypes/>`_
are not what normal people would call an "application", they are
rather "plugins" or "modules".

That said, we have to forgive Django this oddness which has
understandable historical reasons.  After all it is basically just a
vocabulary problem.  Many Django people are more or less aware of that
problem, but it would be really much work to fix it because the word
is used in variables like `app_label` and :setting:`INSTALLED_APPS`.
Too much work for "just a vocabulary" problem.

As a compromise, we suggest to just change the documentation.  We
suggest to differentiate between "app" and "application".  We can
continue to call them "apps", but should refrain from expanding that
word to "application".  Because apps are *not* applications, they are
plugins which we happen to call "app" for historical reasons.  This
rule shouldn't offend even the most conservative Django developer.
Unfortunately, the Django developers did not know about these
considerations when the worked on version 1.7. That's why they
continue to speak about `Applications
<https://docs.djangoproject.com/en/dev/ref/applications/>`_, ignoring
our vocabulary problem.

The "only" problem with this vocabulary problem is that it leaves us
(Lino developers) with no word left for what **we** would want to call
an application.  A Lino application is neither an "app" nor a
"project". 

But that's why we finally use the name "Site" for describing a "Lino
application".



Introducing the :class:`Site` class
===================================

The :class:`Site` is the base class for representing a "Lino
application".  The :class:`Site` class brings an additional level of
encapsulation to Django.  A :class:`Site` *class* is a kind of "master
app" or "project template".  A :class:`Site` *instance* roughly
corresponds to a "project" for Django.


A `Site` has attributes like :attr:`Site.verbose_name` (the "short"
user-visible name) and the :attr:`Site.version` which are used by the
method :meth:`Site.welcome_text`.  It also defines a
:meth:`Site.startup` method and signals which fire exactly once when
the application starts up.

And then it is designed to be subclassed by the application developer
(e.g. :class:`lino.projects.min1.settings.Site`), then imported into a
local :xfile:`settings.py`, where a local system administrator may
subclass it another time.

A Lino application starts to "live" when such a :class:`Site` class
gets **instantiated**.  This instance of your application is then
stored in the :setting:`SITE` variable of a :xfile:`settings.py`.


A `Site` is usually meant to work for a given set of Django apps
(i.e. what's in the :setting:`INSTALLED_APPS` setting).  It is a
"collection of apps" which make up a whole.  To define this
collection, the application developper usually overrides the
:meth:`Site.get_installed_apps` method.

.. currentmodule:: lino.core.plugin

And then Lino has another class, called :class:`Plugin`, which is a
wrapper around a Django app. Lino creates one :class:`Plugin` instance
for every installed app.

The :class:`Plugin` class is comparable to Django's `AppConfig
<https://docs.djangoproject.com/en/1.7/ref/applications/>`_ class
which has been added in version 1.7, but they make certain things
possible which are not possible in plain Django.
