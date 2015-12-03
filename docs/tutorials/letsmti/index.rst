===========================================
A Local Exchange Trade System (MTI version)
===========================================

.. this document is part of the Lino test suite. To test only this
  document, run::

   $ python setup.py test -s tests.DocsTests.test_letsmti


Followup for :doc:`/tutorials/mti/index`.

.. contents::
   :local:



There are two "classes" of Members : Customers and Suppliers. 
A Member can be both a Customer and a Supplier.
Only Customers can have Demands, and only Suppliers can have Offers. 



Now here is the :xfile:`models.py` file which defines these database
models:

.. literalinclude:: models.py



Tables
======

For every database model there should be at least one :class:`Table
<lino.core.dbtables.Table>`. Database *models* are usually named in
*singular* form, tables in *plural* form.

You may define your tables together with the models in your
:file:`models.py` file, but for this tutorial we defined them in a
separate file :file:`tables.py`. It's a matter of taste, but if you
separate them, then you must import the :file:`tables.py` file from
within your :file:`models.py` so that they get imported at startup.

.. literalinclude:: tables.py


Demo data
=========

It is important to get some fictive data which corresponds more or
less to the reality of your customer.  Here is the demo data for this
tutorial.

.. literalinclude:: fixtures/demo.py


As soon as you have written such a fixture, you can start to write
test cases.  The following code snippets are so-called "doctests",
they are both a **visualisation of your demo data** (which you might
show to your customer) and a part of the test suite of your
application (which you invoke with::

  $ python manage.py test

The above command will run the following code snippets in a subprocess
and check whether their output is the same as the one displayed here.

Doctests usually need to do some initialization.

>>> from __future__ import print_function
>>> from lino.api.shell import *
>>> from lino.api import rt

Since doctests run on a temporary database, we need to load our
fixture each time this document is being tested.

>>> from django.core.management import call_command
>>> call_command('initdb', 'demo', interactive=False,verbosity=0)

    
Show the list of members:    

>>> rt.show(letsmti.Members)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ========= ========== =====================
 ID   name      place      email
---- --------- ---------- ---------------------
 1    Fred      Tallinn    fred@example.com
 2    Argo      Haapsalu   argo@example.com
 3    Peter     Vigala     peter@example.com
 4    Anne      Tallinn    anne@example.com
 5    Jaanika   Tallinn    jaanika@example.com
 6    Henri     Tallinn    henri@example.com
 7    Mari      Tartu      mari@example.com
 8    Katrin    Vigala     katrin@example.com
==== ========= ========== =====================
<BLANKLINE>

>>> rt.show(letsmti.Customers)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======== ========= ==================== =================
 ID   name     place     email                customer remark
---- -------- --------- -------------------- -----------------
 6    Henri    Tallinn   henri@example.com
 7    Mari     Tartu     mari@example.com
 8    Katrin   Vigala    katrin@example.com
==== ======== ========= ==================== =================
<BLANKLINE>

>>> rt.show(letsmti.Suppliers)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======== ========== ==================== =================
 ID   name     place      email                supplier remark
---- -------- ---------- -------------------- -----------------
 1    Fred     Tallinn    fred@example.com
 2    Argo     Haapsalu   argo@example.com
 4    Anne     Tallinn    anne@example.com
 6    Henri    Tallinn    henri@example.com
 7    Mari     Tartu      mari@example.com
 8    Katrin   Vigala     katrin@example.com
==== ======== ========== ==================== =================
<BLANKLINE>


Here is how we express these things by defining two methods
:meth:`setup_menu <lino.core.site.Site.setup_menu>` and
:meth:`get_admin_main_items
<lino.core.site.Site.get_admin_main_items>` in our
:xfile:`settings.py` file.

.. literalinclude:: settings.py

We can show the main menu in a doctest:

>>> ses = rt.login()
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Master : members, customers, suppliers, products
- Market : offers, demands
- Configure : places



Form layouts
============

Note the `detail_layout` attributes of certain tables.  



The web interface
=================

Now you are ready to write a "first draft" prototype.  The goal of
such a prototype is to have something to show to your customer that
looks a little bit like the final product, and with wich you can play
to test whether your analysis of the database structure is okay.  

Please explore the files in :srcref:`docs/tutorials/letsmti`, copy them
to a local project directory and try to get the prototype running.

You will need run the following command to populate your database with
some demo data::

  python manage.py initdb_demo
  
Then you start the development web server using::

  python manage.py runserver

And point your browser to http://127.0.0.1:8000/

    

Summary
=======

In this tutorial you learned about **MTI**: 
