Licensing : How to make money with Lino
=======================================

Lino is published under the `GPL
<http://en.wikipedia.org/wiki/GNU_General_Public_License>`_.  The
reason for this choice is explained in :doc:`why_gpl`.  But what does
this mean concretely?  This section explains how the author of Lino
understands the GPL.  It has no legal value, the only authority is the
license text.  Comments and questions are welcome.

The GPL gives you the permission to use Lino as a base 
for your own work. Examples:

- You write your own Lino application.  A Lino application can be
  something as simple as the "Polls" application described in
  :ref:`lino.tutorial.polls`.  You can extend or modify one of the
  existing Lino applications and consider the result as your work.
  
- You write your own collection of Lino plugins, a concurrent to the
  :ref:`modlib`.
  
- You write some other extension to the Lino framework, e.g. a new
  user interface.

- You start a fork which does certain things in a better way.
  
If you do any of the above, then your work is also subject 
to the GPL. Which means that

- you are free to use it for yourself and within your company
- you are encouraged (but not obliged to) share your work to others
- if you share your work, then you must do this according to the terms
  of the GPL (no license fee, source code available, etc.)

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

**What the GPL does not allow** is to share your Lino application
using **another license** than the GPL. Concretely:

- You are not allowed to run your application on a public website
  *without also* distributing your code. This limitation comes because
  Lino uses ExtJS, which is Javascript (client-side code), and in that
  case the `Sencha FAQ <http://www.sencha.com/legal/open-source-faq/>`_
  explains that *“Conveyance” for a web application is triggered when a
  user outside the legal entity that created the application uses the
  application."*

- And the license of your application (if you publish it) must be GPL,
  even BSD or some other FOSS license is not allowed here, since that
  would open the door for a third party to re-use our work under a
  non-free license.

If you want to do one of the above, then you must ask me (and also
Sencha and Ext.ensible) for *another license than the GPL*, and this
license will cost some money.

