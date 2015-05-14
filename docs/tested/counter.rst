.. _lino.tested.counter:

===============================
The `counter` template function
===============================

.. to run only this test:

  $ python setup.py test -s tests.DocsTests.test_counter

.. doctest initialization:

    >>> from __future__ import print_function
    >>> import os
    >>> os.environ['DJANGO_SETTINGS_MODULE'] = 'lino.projects.min1.settings.doctests'
    >>> from lino.api.doctest import *

Why we need it
==============

The problem: In a Jinja template we would like to render a document
with section headers which contain a number, and that number increases
for each section.  Some sections are optional, i.e. they are rendered
only if some context-dependent condition is met.  So the numbers of
the sections are not always the same.

A first approach is to use a macro::

    {%- set artno = 1 -%}
    {%- macro article() -%}
    <h2>Article {{artno}}</h2>
    {%- set artno = artno + 1 -%}
    {%- endmacro -%}
    
And then to have this in our template::    
    
    {%- if ... -%}
    {{article()}}
    <p>Bla bla...</p>
    {%- endif ... -%}

    {%- if ... -%}
    {{article()}}
    <p>Bla bla...</p>
    {%- endif ... -%}

    {%- if ... -%}
    {{article()}}
    <p>Bla bla...</p>
    {%- endif ... -%}

Unfortunately this trick does not work because the macro does not see
the global variable.

So Lino adds a custom function called ``counter`` to its global Jinja
environment which can be used to easily insert incrementing counters
into a document.

Usage
=====

Using the `counter` function in your template is easy:

>>> s = "Easy as {{counter()}}, {{counter()}} and {{counter()}}!"

Here is how this template will render :

>>> tpl = settings.SITE.jinja_env.from_string(s)
>>> print(tpl.render(settings.SITE.get_printable_context()))
Easy as 1, 2 and 3!

If you need more than one counter, then you can name them by passing a
first optional parameter:

>>> s = "{{counter('h1')}} {{counter('h1')}} {{counter('h2')}} {{counter('h1')}} {{counter('h2')}}"
>>> tpl = settings.SITE.jinja_env.from_string(s)
>>> print(tpl.render(settings.SITE.get_printable_context()))
1 2 1 3 2

The ``counter`` function has an optional argument `value` which you can
use to specify a start value:

>>> s = "{{counter(value=3)}} {{counter()}} {{counter()}} and {{counter(value=1)}} {{counter()}} "
>>> tpl = settings.SITE.jinja_env.from_string(s)
>>> print(tpl.render(settings.SITE.get_printable_context()))
3 4 5 and 1 2 

The ``counter`` function also has an optional argument `step` which
defines the value to add to the current value (don't ask me why
somebody would use this):

>>> s = "Easy as {{counter(step=2)}}, {{counter(step=2)}} and {{counter(step=2)}}!"
>>> tpl = settings.SITE.jinja_env.from_string(s)
>>> print(tpl.render(settings.SITE.get_printable_context()))
Easy as 2, 4 and 6!


Where counters are being stored
===============================

Jinja template functions may not modify the context, so how do we
store the list of counters and their current value? The `counter`
function simply uses a context variable named ``inc_counters``, which
must exist in the context and hold an empty `dict`.  In Lino this
happens automatically since every rendering of a template calls the
Site's :meth:`get_printable_context
<lino.core.site.Site.get_printable_context>` method, and this method
defines this ``inc_counters`` variable.

If you render it a second time, you must call
:meth:`get_printable_context
<lino.core.site.Site.get_printable_context>` again in order to reset
all counters.

So we can define and compile a template *once*:

>>> s = "Easy as {{counter()}}, {{counter()}} and {{counter()}}!"
>>> tpl = settings.SITE.jinja_env.from_string(s)

And then render it several times:

>>> print(tpl.render(settings.SITE.get_printable_context()))
Easy as 1, 2 and 3!
>>> print(tpl.render(settings.SITE.get_printable_context()))
Easy as 1, 2 and 3!

Or if you want the counters to persist? In that case you can simply
reuse the context returned by :meth:`get_printable_context
<lino.core.site.Site.get_printable_context>`:

>>> ctx = settings.SITE.get_printable_context()
>>> print(tpl.render(ctx))
Easy as 1, 2 and 3!
>>> print(tpl.render(ctx))
Easy as 4, 5 and 6!


