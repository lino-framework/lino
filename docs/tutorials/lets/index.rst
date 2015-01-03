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


We also define detail layouts for **Member**::

    class Members(dd.Table):
        model = Member

        detail_layout = """
        id name place email
        OffersByMember DemandsByMember
        """


The content of the main page
============================

Another thing to discuss with your customer during :doc:`analysis
</team/analysis>` is: what information should be on the main page of
your application.

We imagine that they want the main page to display a simple catalog of
the things available for exchange.


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




The first prototype
===================

Now you are ready to write a "first draft" prototype.  The goal of
such a prototype is to have something to show to your customer that
looks a little bit like the final product, and with wich you can play
to test whether your analysis of the database structure is okay.  

The code for such a first draft is in :srcref:`docs/tutorials/lets`.
Please explore these files:
 
=================================================================== =========================
:srcref:`models.py </docs/tutorials/lets/models.py>`                defines the database models and tables
:srcref:`settings.py </docs/tutorials/lets/settings.py>`            contains the main menu and other application settings
:srcref:`manage.py </docs/tutorials/lets/manage.py>`                (you may need to adapt this so that it sets a correct value for `DJANGO_SETTINGS_MODULE`)
:srcref:`fixtures/demo.py </docs/tutorials/lets/fixtures/demo.py>`  defines demo data
=================================================================== =========================


Now copy these files to a local project directory and try to get the
prototype running.

First you must run the following command to populate your database
with some demo data::

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
