Using Lino to write a proprietary application
=============================================

.. note::

   Disclaimer: This section has no legal value, the only authority is 
   the license text.  Comments and questions are welcome.

Lino is published under the `LGPL
<http://en.wikipedia.org/wiki/GNU_Lesser_General_Public_License>`_.
If you use Lino to write your own application, we encourage you to
make it free software by publishing it using the GPL.

If you want to run a proprietary Lino application for usage by a
`"non-employee of the legal entity that created the application"
<http://www.sencha.com/legal/open-source-faq>`__), e.g. on an 
`SaaS <http://en.wikipedia.org/wiki/Software_as_a_service>`_
site, then you potentially **need to purchase a commercial license for
the following Javascript libraries** which your Lino application needs
to run:

- Most Lino applications include :mod:`lino.modlib.extjs` and thus
  need the `Sencha ExtJS Javascript framework
  <http://www.sencha.com/products/extjs/>`_ when running.

- If your application includes :mod:`lino.modlib.extensible`, then it
  also needs the `Calendar Pro <http://ext.ensible.com/>`_ Javascript
  library from Ext.ensible.

Note that neither Sencha nor Ext.ensible want any money from you if
your application is itself GPL.

Note also that *for Lino* there is no additional license necessary in
the above cases. You don't need to contact me nor to pay me any
money. But you must check yourself whether you need the above licenses
and, if yes, contact their respective vendors.

It is possible to write Lino applications which do not need either of
these Javascript frameworks. For example :ref:`belref`. Such
applications don't require any additional license even if they are
proprietary.

