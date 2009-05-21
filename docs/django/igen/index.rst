igen -- invoice generator
=========================

"igen" stands for "invoice generator" and is a simple, 
web-based program to write invoices either manually or 
periodically based on contracts.
It should become the first Lino Django 
application. 
There is even an early `demo site <http://igen.saffre-rumma.ee>`_ 

Module :mod:`lino.django.igen`.

.. module:: lino.django.igen.models


Generating invoices
-------------------

There will be a command-line script and/or a Dialog that launches the 
invoice generation process. 
This basically loops over the existing Orders, asking them whether they 
need an invoice. 

:meth:`Order.make_invoice` creates an :class:`Invoice` for this Order
at the specified date :attr:`today`.
Returns the created Invoice instance or None if no invoice needs to be
created.

If for some reason there were no invoice issued during more than a
cycle, then the generated invoice must cover a longer period. 
How to handle this?

We could add two date fields `Invoice.covers_from` and
`Invoice.covers_until` to each invoice. But this sounds paranoid...

So we adopted the following approach: 

A field ''Order.covered_until'' tells whether it is time to send an
invoice (''today + 5 < Order.covered_until'').
This field is then incremented when an invoice is created.
The covered period is indicated as a comment in the generated invoice.
If the moderator deletes the generated invoice, then it is her
responsibility to adjust `Order.covered_until`.
        
