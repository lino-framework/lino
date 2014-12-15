.. _lino.tutorial.lets:

=============================
A Local Exchange Trade System
=============================

In this tutorial we are going to write a new Lino application from
scratch.  It is an application to manage a Local Exchange Trade System
(`LETS
<http://en.wikipedia.org/wiki/Local_exchange_trading_system>`_),
inspired by a real web site http://www.elavtoit.com

Analysis
========

Imagine that you have interviewed your future customer and analyzed
their needs.  Your analyze must result in the description of (at
least) three things:

- a database structure
- a menu structure
- the layout of detail forms

Database structure
------------------

You translated their needs into the following description of their
database structure:

- **Products** : one row for every product. We keep it simple and just
  record the designation for our products. We don't even record a
  price.

- **Providers** : a list of people who provide one or several
  products. For each provider we record their contact data such as
  place and email.

- **Customers** : a list of people who are actively looking for one or
  several products. For each customer we record their contact data
  such as place and email.

- An **Offer** is when a given Provider offers a given Product.

- A **Demand** is when a given Customer is actively loking for a given
  Product.

Here is a graphical representation of that strucure:

.. digraph:: foo

   "Offer" -> "Product";
   "Demand" -> "Product";
   "Offer" -> "Provider";
   "Demand" -> "Customer";
   "Provider" ->  "Place";
   "Customer" ->  "Place";

Note that every arrow on this picture will become a `ForeignKey` in
our :xfile:`models.py`.

Menu structure
--------------

Another thing which we must do is to design a menu structure. Imagine
that they want something like this:

- **Master** contains "master data" (i.e. relatively stable data):

  - Products -- open the list of products
  - Customers -- open the list of customers
  - Providers  -- open the list of providers

- **Market**

  - Offers  -- open the full list of all offers
  - Demands  -- open the full list of all demands

Form layouts
------------

For certain database objects your application should define a **detail
window**.  A detail window is what Lino opens when the user
double-clicks on a given row.

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


We also define detail layouts for **Customer** and for **Provider**::

    class Providers(dd.Table):
        model = Provider

        detail_layout = """
        id name place email
        OffersByProvider
        """

    class Customers(dd.Table):
        model = Customer

        detail_layout = """
        id name place email
        DemandsByCustomer
        """


The first prototype
===================

Now you are ready to write a "first draft" prototype.  The goal of
such a prototype is to have something to show to your customer that
looks a little bit like the final product, and with wich you can play
to test whether your analysis of the database structure is okay.  

The code for such a first draft is in :srcref:`/lino/tutorials/lets1`.
Please explore these files:
 
=================================================================== =========================
:file:`__init__.py`                                                 (empty file)
:srcref:`settings.py </lino/tutorials/lets1/settings.py>`           contains the main menu and other application settings
:srcref:`manage.py </lino/tutorials/lets1/manage.py>`               (you may need to adapt this so that it sets a correct value for `DJANGO_SETTINGS_MODULE`)
:file:`lets/__init__.py`                                            (empty file)
:srcref:`lets/models.py </lino/tutorials/lets1/lets/models.py>`     defines the database models
:file:`fixtures/__init__.py`                                        (empty file)
:srcref:`fixtures/demo.py </lino/tutorials/lets1/fixtures/demo.py>` defines demo data
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
