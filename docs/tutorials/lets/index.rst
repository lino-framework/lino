.. _lino.tutorial.lets:

=============================
A Local Exchange Trade System
=============================

In this tutorial we are going to write a new Lino application from
scratch.

Our application is a website of a Local Exchange Trade System (`LETS
<http://en.wikipedia.org/wiki/Local_exchange_trading_system>`_). The
members of that site would register the products and services they
want to sell or to buy. The goal is to connect the providers and the
customers.


.. contents::
   :local:


Database structure
==================

We imagine that you (or some other team member) have :doc:`analyzed
</team/analysis>` the needs of your future customer and want the
following database structure:

- **Products** : one row for every product or service. We keep it
  simple and just record the designation for our products. We don't
  even record a price.

- **Members** : the people who use this site to register their offers
  and demands. For each member we record their contact data such as
  place and email.

- An **Offer** is when a given member declares that they want to *sell*
  a given product.

- A **Demand** is when a given member declares that they want to *buy* a
  given product.

Here is a graphical representation of that structure:


.. digraph:: foo

   node [shape=box, fontname="Helvetica"];  Product;
   node [shape=box];  Offer, Demand;
   node [shape=box, fontname="Helvetica"];  Member, Place;

   Offer -> Product;
   Demand -> Product;
   Offer -> Member;
   Demand -> Member;
   Member ->  Place;


Notes:

- Every **arrow** on the diagram represents a `ForeignKey` in our
  :xfile:`models.py`. This way of representing a database structure is a
  bit uncommon, but we find it to be intuitive and useful. 

- There are two `many-to-many relationships
  <https://docs.djangoproject.com/en/1.7/topics/db/examples/many_to_many/>`_
  between Member and Product which we might call "offered" and
  "wanted".  You might define something like this::
  
    class Member(Model):
        offered_products = ManyToManyField(Product, through=Offer)
        wanted_products = ManyToManyField(Product, through=Demand)

- We don't pretend that this structure is actually useful, optimal an
  cool.  Actually it's a bit too simple.  But we *imagine* that this
  is what our customer *asks* us to do.


:srcref:`models.py </docs/tutorials/lets/models.py>`                defines the database models and tables


.. literalinclude:: models.py


Form layouts
============

Another thing to discuss with your customer during :doc:`analysis
</team/analysis>` is the **layout** of the **detail window** for
certain database models.  A detail window is what Lino opens when the
user double-clicks on a given row.

.. textimage:: t3a-3.jpg
    :scale: 50%

    The detail window of a **Product** should show the data fields and
    two slave tables, one showing the the **offers** and another with
    the **demands** for this product.

    Here is the code for this::

        detail_layout = """
        id name
        OffersByProduct DemandsByProduct
        """
    
When seeing the code on the left, you should be able to imagine
something like the picture on the right.

Layouts are defined per *table*, not per *model*.

I usually define my tables directly in my :file:`models.py` file, but
for this tutorial I defined them in a separate file
:file:`tables.py`. It's a matter of taste, but if you separate them,
then you must take car that they get imported from within your
:file:`models.py`.

.. literalinclude:: tables.py



Menu structure
==============

And a last thing to discuss with your customer during :doc:`analysis
</team/analysis>` is the **menu structure**. We imagine that they want
something like this:

- **Master** contains "master data" (i.e. relatively stable data):

  - Products -- show the list of products
  - Members -- show the list of members

- **Market**

  - Offers  -- show the full list of all offers
  - Demands  -- show the full list of all demands


We imagine that they want the main page to display a simple catalog of
the things available for exchange.

.. literalinclude:: settings.py


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
>>> from lino.runtime import *
>>> from lino import rt

Since doctests run on a temporary database, we need to load our
fixture each time this document is being tested.

>>> from django.core.management import call_command
>>> call_command('initdb', 'demo', interactive=False)
Creating tables ...
Creating table lets_place
Creating table lets_member
Creating table lets_product
Creating table lets_offer
Creating table lets_demand
Installing custom SQL ...
Installing indexes ...
Installed 21 object(s) from 1 fixture(s)

    
Show the list of members:    

>>> rt.show(lets.Members)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ========= ========== =======
 ID   name      place      email
---- --------- ---------- -------
 1    Fred      Tallinn
 2    Argo      Haapsalu
 3    Peter     Vigala
 4    Anne      Tallinn
 5    Jaanika   Tallinn
 6    Henri     Tallinn
 7    Mare      Tartu
 8    Katrin    Vigala
==== ========= ========== =======
<BLANKLINE>

Show the list of products:    

>>> rt.show(lets.Products)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
=========== ==================== =====================
 name        Offered by           Wanted by
----------- -------------------- ---------------------
 Bread       **Fred**
 Buckwheat   **Fred**, **Anne**   **Henri**
 Eggs                             **Henri**, **Mare**
=========== ==================== =====================
<BLANKLINE>

Show the list of offers:    

>>> rt.show(lets.Offers)
... #doctest: +NORMALIZE_WHITESPACE +REPORT_UDIFF
==== ======== =========== =============
 ID   member   product     valid until
---- -------- ----------- -------------
 1    Fred     Bread
 2    Fred     Buckwheat
 3    Anne     Buckwheat
==== ======== =========== =============
<BLANKLINE>


Show the main menu:

>>> ses = rt.login()
>>> ses.show_menu()
... #doctest: +ELLIPSIS +NORMALIZE_WHITESPACE +REPORT_UDIFF
- Master : members, products
- Market : offers, demands
- Configure : places


The web interface
=================

Now you are ready to write a "first draft" prototype.  The goal of
such a prototype is to have something to show to your customer that
looks a little bit like the final product, and with wich you can play
to test whether your analysis of the database structure is okay.  

Please explore the files in :srcref:`docs/tutorials/lets`, copy them
to a local project directory and try to get the prototype running.

You will need run the following command to populate your database with
some demo data::

  python manage.py initdb_demo
  
Then you start the development web server using::

  python manage.py runserver

And point your browser to http://127.0.0.1:8000/

Here are some screenshots.

.. image:: t3a-1.jpg
    :scale: 70
    
.. image:: t3a-2.jpg
    :scale: 70
    
.. image:: t3a-3.jpg
    :scale: 70


Conclusion
==========

We hope that this encourages you to start writing your own Lino
application.
