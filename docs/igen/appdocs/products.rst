========
products
========



.. currentmodule:: products

Defined in :srcref:`/lino/modlib/products/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; ProductCat

.. _std.products.ProductCat:

--------------------
Model **ProductCat**
--------------------




    
  
=========== ============== ============
name        type           verbose name
=========== ============== ============
id          AutoField      ID          
name        BabelCharField name        
description TextField      description 
name_de     CharField      name (de)   
name_fr     CharField      name (fr)   
name_nl     CharField      name (nl)   
name_et     CharField      name (et)   
=========== ============== ============

    
Defined in :srcref:`/lino/modlib/products/models.py`

.. index::
   single: field;id
   
.. _std.products.ProductCat.id:

Field **ProductCat.id**
=======================





Type: AutoField

   
.. index::
   single: field;name
   
.. _std.products.ProductCat.name:

Field **ProductCat.name**
=========================





Type: BabelCharField

   
.. index::
   single: field;description
   
.. _std.products.ProductCat.description:

Field **ProductCat.description**
================================





Type: TextField

   
.. index::
   single: field;name_de
   
.. _std.products.ProductCat.name_de:

Field **ProductCat.name_de**
============================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _std.products.ProductCat.name_fr:

Field **ProductCat.name_fr**
============================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _std.products.ProductCat.name_nl:

Field **ProductCat.name_nl**
============================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _std.products.ProductCat.name_et:

Field **ProductCat.name_et**
============================





Type: CharField

   


.. index::
   pair: model; Product

.. _std.products.Product:

-----------------
Model **Product**
-----------------



Product(id, name, description, cat_id, vatExempt, price, name_de, name_fr, name_nl, name_et, description_de, description_fr, description_nl, description_et)
  
============== ============== ================
name           type           verbose name    
============== ============== ================
id             AutoField      ID              
name           BabelCharField name            
description    BabelTextField description     
cat            ForeignKey     Category        
vatExempt      BooleanField   vatExempt       
price          PriceField     price           
name_de        CharField      name (de)       
name_fr        CharField      name (fr)       
name_nl        CharField      name (nl)       
name_et        CharField      name (et)       
description_de TextField      description (de)
description_fr TextField      description (fr)
description_nl TextField      description (nl)
description_et TextField      description (et)
============== ============== ================

    
Defined in :srcref:`/lino/modlib/products/models.py`

.. index::
   single: field;id
   
.. _std.products.Product.id:

Field **Product.id**
====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _std.products.Product.name:

Field **Product.name**
======================





Type: BabelCharField

   
.. index::
   single: field;description
   
.. _std.products.Product.description:

Field **Product.description**
=============================





Type: BabelTextField

   
.. index::
   single: field;cat
   
.. _std.products.Product.cat:

Field **Product.cat**
=====================





Type: ForeignKey

   
.. index::
   single: field;vatExempt
   
.. _std.products.Product.vatExempt:

Field **Product.vatExempt**
===========================





Type: BooleanField

   
.. index::
   single: field;price
   
.. _std.products.Product.price:

Field **Product.price**
=======================





Type: PriceField

   
.. index::
   single: field;name_de
   
.. _std.products.Product.name_de:

Field **Product.name_de**
=========================





Type: CharField

   
.. index::
   single: field;name_fr
   
.. _std.products.Product.name_fr:

Field **Product.name_fr**
=========================





Type: CharField

   
.. index::
   single: field;name_nl
   
.. _std.products.Product.name_nl:

Field **Product.name_nl**
=========================





Type: CharField

   
.. index::
   single: field;name_et
   
.. _std.products.Product.name_et:

Field **Product.name_et**
=========================





Type: CharField

   
.. index::
   single: field;description_de
   
.. _std.products.Product.description_de:

Field **Product.description_de**
================================





Type: TextField

   
.. index::
   single: field;description_fr
   
.. _std.products.Product.description_fr:

Field **Product.description_fr**
================================





Type: TextField

   
.. index::
   single: field;description_nl
   
.. _std.products.Product.description_nl:

Field **Product.description_nl**
================================





Type: TextField

   
.. index::
   single: field;description_et
   
.. _std.products.Product.description_et:

Field **Product.description_et**
================================





Type: TextField

   


