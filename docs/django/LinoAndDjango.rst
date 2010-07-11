Lino and Django
===============

When in the end of 2008 I discovered Django, I was quickly seized by
its clear design and mature implementation.
The ORM and database model based on "applications" is simply genial.
The way of how this is integrated into a web application server system: genial.

Only one thing disturbed me: the 
`admin application <http://docs.djangoproject.com/en/dev/ref/contrib/admin/#ref-contrib-admin>`_  
has obviouslynever been designed to write complete database applications.
That's why I started to write Lino.
Yes, Lino is an alternative for one of Django's flagships, the `django.contrib.admin` module.


How I'd explain Lino to Django developers
-----------------------------------------

Lino, when ready, will be a possible answer to what Jacob Kaplan-Moss writes in 
`What The Enterprise wants from Django <http://groups.google.com/group/django-developers/browse_thread/thread/c89e028a536514d3?hl=en&pli=1>`_:

  "(Django) doesn't really have a good answer for the people who want
  something IDE or GUI-ish. Meanwhile, Adobe and Microsoft are putting
  all sorts of marketing dollars into Flex/Silverlight, and although
  HTML5 can do some amazing things, the lack of tooling is a big danger.
  (I've written at more length about this in the past:
  http://jacobian.org/writing/snakes-on-the-web/#s-rich-web-applications)." 

Here is a recent screenshot of a Lino application:

.. image:: http://lino.googlecode.com/hg/screenshots/20100207.jpg
  :width: 50%
  :target: http://lino.googlecode.com/hg/screenshots/20100207.jpg

Lino integrates to your site through the `urls.py` in a similar way than Admin does::

  from lino import lino_site
  urlpatterns = patterns('',
      (r'', include(lino_site.get_urls())),
  )    

Lino sites are normal Django sites, but your :setting:`INSTALLED_APPS` will usually contain applications designed to use Lino.

Lino applications are basically normal Django applications, but 
instead of writing `Admin` classes for your Django models, you write Reports, Layouts and Actions. You'll define these classes in your application's 'models' module.

Reports describe something that the user will see as a 
Window with a Grid as main component.

Layouts are my self-made approach to design entry forms in a GUI-independent way.
Users see them as Tabs of a Detail window (whose main component is a 
[http://www.extjs.com/deploy/dev/examples/form/xml-form.html FormPanel])

Instead of having each application register its models to the admin site, you write a main menu for your site that uses your Reports and Actions. This is is currently done in a file `lino_settings.py`, usually in the same directory as Django's `settings.py`.
This approach is less pluggable than Admin-based applications, but enterprise solutions don't need to be plug and play.


Lino currently makes extensive use of :term:ExtJS,
but it is possible to write other interfaces in the future. I can imagine simple HTML, curses, Qt, but at the moment I am just satisfied with ExtJS.