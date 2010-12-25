iGen User Manual
================

About iGen
----------

iGen is a web application for writing invoices to customers and
managing their payments. 

You may use the demo site 
http://igen-demo.saffre-rumma.net/
as a sandbox.

The demo database contains fictive data. 
You can change this data and play with it, the database is being reset when necessary. 

When you visit the demo site for the first time, 
you must log in as "root" or "user".
Both users have "1234" as password.
The login link is situated in the upper right corner.

The menu changes depending on who you are.
There are currently four levels of users: anonymous, normal, staff and root.

  - Anonymous users can see our products. 
  - Normal users can create, change and delete their own orders. 
  - Staff users can do almost everything.


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
        
