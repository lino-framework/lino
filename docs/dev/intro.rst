============
Introduction
============

Lino applications are basically normal Django applications, but 
instead of writing `Admin` classes for your Django models, you write Reports 

A Report describes a set of tabular data
independently of *user interface* and *medium* (paper, screen, interactive or not), 
but with all the meta-data information necessary for any user interface 
to produce a satisfying result on any medium.
This is the theory.

Because we don't yet have carefully selected examples, 
we suggest here that you look at the code of the :mod:`lino.modlib.contacts` 
module which should be relatively self-explanatory.
For example :srcref:`/lino/lino/modlib/contacts/models.py`

Your Reports are subclasses of :class:`lino.reports.Report`, and they 
must be defined in your application's 'models' module because Lino 'discovers' 
and instantiates them automatically at startup.

You will also define Layouts for your detail forms.

A Layout describes an entry form in a GUI-independent way.
Users see them as Tabs of a Detail window (whose main component is a 
`FormPanel <http://www.extjs.com/deploy/dev/examples/form/xml-form.html>`_)

Instead of having each application register its models to the admin site, 
you write a main menu for your site that uses your Reports. 
This is is currently done in a file :xfile:`lino_settings.py`, 
usually in the same directory as Django's :xfile:`settings.py`.
This approach is less pluggable than Admin-based applications, 
but enterprise solutions don't need to be plug and play.

