License
=======

.. note::

   Disclaimer: This section explains how we understand the LGPL.  It
   has no legal value, the only authority is the license text.
   Comments and questions are welcome.

Lino is published under the `LGPL
<http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License>`_
because we want to make sure that our work will always remain free
software and never be controlled by some proprietary organisation.

The LGPL gives you the permission to use Lino as a base for your own
work. Examples:

- You write your own Lino application.  A Lino application can be
  something as simple as the "Polls" application described in
  :ref:`lino.tutorial.polls`.  You can extend or modify one of the
  existing Lino applications and consider the result as your work.
  
- You write your own collection of Lino apps, a concurrent to the
  :ref:`modlib`.
  
- You write some other extension to the Lino framework, e.g. a new
  user interface.

Making money with free software
-------------------------------

If you do any of the above, then we encourage you to make your derived
work free software by publishing it using the GPL or LGPL.

You may do all this as a *commercial activity*.  When working with
free software, you make money by selling *your work*, not by selling
*the permission to use* your work (aka license).  The trick is to
understand the basic message of the GPL: **spiritual work is no
private property and cannot be used as capital**.

Here are some ideas on how to use Lino for making money:

- you write an in-house Lino application for your customer.  The GPL
  can then act as a warranty for your customer that you are not going
  to reuse their know-how and sell it to another customer.

- you sell mass hosting for some of the existing Lino applications

- you sell support for an existing Lino application

- you organize seminars for Lino end-users or system administrators

You do not need to register nor to pay me for doing these things.  Of
course I recommend that you inform me about your activity and to
register at least to the announcement mailing list.  And maybe I will
offer you to pay me money for getting my professional support.  But
these are not requirements.

Using Lino to write non-free software
-------------------------------------

Let's imagine that you take :ref:`cosi`, get it running on your
server, invest considerable time to fix bugs and add more features.
And then you run your improved version of :ref:`cosi` on your `SaaS
<http://en.wikipedia.org/wiki/Software_as_a_service>`_ site *without*
publishing the source code.

More generally speaking, you want to run a proprietary Lino
application for usage by a `"non-employee of the legal entity that
created the application"
<http://www.sencha.com/legal/open-source-faq>`__).

Because Lino is LGPL (and not GPL), it permits this kind of
usage. *For Lino* there is no additional license necessary. You don't
need to contact me nor to pay me any money.  But you must check
yourself whether you **need to purchase a commercial license for the
following Javascript libraries** and, if yes, contact their respective
vendors:

- Most Lino applications include :mod:`lino.modlib.extjs` and thus
  need the `Sencha ExtJS Javascript framework
  <http://www.sencha.com/products/extjs/>`_ when running.

- If your application includes :mod:`lino.modlib.extensible`, then it
  also needs the `Calendar Pro <http://ext.ensible.com/>`_ Javascript
  library from Ext.ensible.

Notes:

- Neither Sencha nor Ext.ensible want any money from you if your
  application is itself GPL or LGPL (or any other less restrictive
  open source licence as mentionned in `Exception for Development
  <http://www.sencha.com/legal/open-source-faq/open-source-license-exception-for-development/>`_.

- It is possible to write Lino applications which do not need either
  of these Javascript frameworks. For example :ref:`belref`. Such
  applications don't require any additional license even if they are
  proprietary.


Why Lino is not BSD licensed
----------------------------

I imagine you are a Python programmer and want to write some
commercial software package, and you want to use Lino as a framework.
Concretely you will write Python code which imports things from
Lino. That's okay and that's what I wanted to make possible by
switching from GPL to LGPL.

The LGPL (unlike the BSD) then says that you may *not* make a copy of
Lino *itself* or any part of it and turn it into proprietary software.

Let's imagine for example that you don't use Lino but stumble over my
:ref:`lino.tutorial.human` tutorial and want to use this in a
proprietary plain Django application.  Simply importing it would be
okay.  But you can't do that directly because it requires the
:class:`ChoiceList <dd.ChoiceList>` class, an
integral part of Lino. You then start to work many hours, and because
you are smart, you manage to reimplement the :class:`ChoiceList
<dd.ChoiceList>` concept without requiring Lino,
you have rewritten a new and better implementation of my
:mod:`lino.mixins.human` module.  And now you want to use this in a
proprietary package?  Sorry, you will need to prove that you did *not*
copy any part of Lino.  And that should be rather difficult because
*of course* (every Python programmer can confirm it) you have been
looking at my source code, and *of course* you have been copying parts
of it."  You may hide your deed by changing variable names,
reorganizing or obfuscating your code and so on, but I (or rather some
of my successors, because I personally don't imagine that I would
waste my time with this kind of activity) might discover your product
and suspect you of the above and try to prove that you did so.  So you
won't do that if you are a professional.

I say "Sorry, this is *not* what we wanted to happen when we invested
our time and energy into Lino!".  The LGPL helps to protect Lino from
this kind of usage.

Possible questions:

- But where is the limit between these two usages?  Aren't the example
  files and tutorials a part of Lino, too?  

  That's why example files don't have an LGPL copyright header. The
  lack of a copyright header indicates that that you may copy it and
  base even non-free work on it.

- But for example the :ref:`lino.tutorial.dpy` tutorial invites me to
  have a look at and get inspired by certain fixture files, and these
  files *do* have a copyright header.  

  In general one can say: as long as your proprietary application
  *uses* Lino, there's no danger. The dangerous thing is to *not* use
  Lino but to offer some proprietary product which looks suspiciously
  similar to Lino.


Why MIT/BSD developers are excluded
-----------------------------------

The author of `How To Care If BSD, MIT, or GPL Licenses Are Used
<http://techblog.ironfroggy.com/2009/07/how-to-care-if-bsd-mit-or-gpl-licenses.html>`_
formulates why he would like Lino to switch from LGPL to BSD:

  If you release some GPL code, I probably can't use it. (...) maybe
  you don't care if I can't use it, but isn't that why you're
  releasing it?  (...)  you're also keeping honest, open source
  enthusiastic developers from using your project. You aren't limiting
  us for technical or legal reasons, but only for our choice of
  another license.

The previous section explains how we don't want Lino to be misused for
producing a *proprietary* concurrent of itself.  Now imagine that you
are honest and enthusiastic and write a better Lino, and that we would
allow you to publish your derivated work under a BSD or MIT license.

The danger then is that some *dishonest* and *powerful* corporation
might now discover your version of Lino and write a proprietary
product based on it.  Your intermediary *free* Lino would have
prepared the making of a *proprietary* Lino.  We don't want this to
happen.  

Yes, indeed, the LGPL is keeping some honest open source enthusiastic
developers from using Lino.  Because they refuse to see the danger and
we refuse to expose our work to the danger.  We want to make sure that
our work will always remain free software and never be controlled by
some proprietary organisation.  That's why Lino is LGPL and not BSD.


A question of belief
--------------------

If you continue to not agree with our choice of the LGPL, then read on. 

We said that you "refuse to see the danger", but this is of course not
a final verdict, it is just our current *credo*.  We *believe* that a
non-free concurrent *is* a serious danger for Lino, while you
*believe* that it *is not*.

Here are some statements which might help us to continue our dialog.

.. complextable::

   BSD/MIT
   <NEXTCELL>
   GPL
   <NEXTROW>
    
   The **user** of the software must be free
   <NEXTCELL>
   The **software** must be free
   <NEXTROW>

   the default state of the product of the intellect should be one of
   freedom to deal with it as one sees fit, implying that you may do what
   you will with what you have in your possession -- and that the same
   applies to everyone else.
   (`wikivs.com <http://www.wikivs.com/wiki/Copyfree_vs_Copyleft>`_)
    
   <NEXTCELL>

   the product of the intellect must be spread as broadly as possible,
   such that distributing the pragmatically useful part of something
   without also distributing the underlying construction of it is
   punishable by law.
   (`wikivs.com <http://www.wikivs.com/wiki/Copyfree_vs_Copyleft>`_)

   <NEXTROW>
    
   liberal, capitalistic
   <NEXTCELL>
   communist

   <NEXTROW>
   
   Companies are more trustworthy than governments because they are
   at least controlled by the governments, while governments have no
   supervising instance.
   
   <NEXTCELL>
   
   Companies are not trustworthy because their declared goal is to
   produce benefit for their owners, not the freedom and well-being of
   their customers.

