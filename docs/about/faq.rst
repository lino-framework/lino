==========================
Frequently Asked Questions
==========================

**Why can't we use plain Django do develop our application?**

Nobody uses *plain* Django. 
Django application developers 
always use Django *together with*
their "portfolio" of "add-ons".
For example 
`Jinja <http://jinja.pocoo.org/>`_, 
`South <http://south.aeracode.org/>`_, 
`bootstrap <http://twitter.github.com/bootstrap/>`_, 
`jQuery <http://jquery.com/>`_, 
`ExtJS <http://www.sencha.com/products/extjs/>`_, 
`Memcached <http://memcached.org/>`_
...
There are many add-ons to Django, and Lino is just one of them.

Django is not designed to provide out-of-the-box solutions.
Developing a Django application means that you are going 
to either write a set of html templates and css files from scratch, 
or copy and paste them from some other project.

Lino applications are much more out-of-the-box.
For example you don't need to write a single html template
and you don't need to `design your URLs
<https://docs.djangoproject.com/en/1.4/topics/http/urls/>`_ 
because we've done this work for you.
Of course you are less flexible. Letting others do some work 
always means that you trust them to make certain decisions.

Read more in :doc:`lino_and_django`

**Can I use Lino together with my existing Django add-on?**

You can use plain Django models that were not written for Lino
and add a Lino-style user interface for them to integrate them 
into a Lino application.
You can then gradually convert your Django models to make 
them more "Lino-like". See :class:`lino.core.Model` 
to see what Lino adds to Django models.

You can override Lino's default URL schema, 
adding it to an existing Django site.
You can even run Lino together with a Django admin.

**We don't like to depend on a one-man framework.**

If you don't want to depend on a single person, 
then help me to build a team or network of Python programmers 
who are able to continue my work and give support for Lino. 

After 20 years of experience I know that Lino will survive 
only if other developers join the project.
I also know that it will take time to find and convince them.

**As a developer, why should I invest time to learn another 
one-man framework?**

Because Lino is so great. It is not yet perfect, but promising ;-)

Note the ;-) behind this statement.
As the author and spiritual father of Lino, 
I love my child and believe in it, 
and it is difficult to find objective answers to this question.
You'll need to judge yourself whether you can share my 
fascination and love for Lino.
Let me try nevertheless to give you some thought input.

Yes, there are many other more or less similar one-man frameworks.

(...)


