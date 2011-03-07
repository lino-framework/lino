========
products
========



.. currentmodule:: products

Defined in :srcref:`/lino/modlib/products/models.py`




.. index::
   pair: model; ProductCat
   single: field;id
   single: field;name
   single: field;description
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et

.. _igen.products.ProductCat:

--------------------
Model ``ProductCat``
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
   pair: model; Product
   single: field;id
   single: field;name
   single: field;description
   single: field;cat
   single: field;vatExempt
   single: field;price
   single: field;name_de
   single: field;name_fr
   single: field;name_nl
   single: field;name_et
   single: field;description_de
   single: field;description_fr
   single: field;description_nl
   single: field;description_et

.. _igen.products.Product:

-----------------
Model ``Product``
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


