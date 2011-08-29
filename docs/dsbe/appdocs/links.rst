=====
links
=====



.. currentmodule:: links

Defined in :srcref:`/lino/modlib/links/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; LinkType

.. _lino.links.LinkType:

------------------
Model **LinkType**
------------------



Implements :class:`links.LinkType`.
  
==== ========= ============
name type      verbose name
==== ========= ============
id   AutoField ID          
name CharField Name (Nom)  
==== ========= ============

    
Defined in :srcref:`/lino/modlib/links/models.py`

Referenced from
`lino.links.Link.type`_



.. index::
   single: field;id
   
.. _lino.links.LinkType.id:

Field **LinkType.id**
=====================





Type: AutoField

   
.. index::
   single: field;name
   
.. _lino.links.LinkType.name:

Field **LinkType.name**
=======================





Type: CharField

   


.. index::
   pair: model; Link

.. _lino.links.Link:

--------------
Model **Link**
--------------



Link(id, user_id, person_id, company_id, type_id, date, url, name)
  
======= ============= ===================================
name    type          verbose name                       
======= ============= ===================================
id      AutoField     ID                                 
user    ForeignKey    User (Benutzer,Utilisateur)        
person  ForeignKey    Person (Personne)                  
company ForeignKey    Company (Firma,Société)            
type    ForeignKey    Link type (Verweisart,Type de lien)
date    DateTimeField Date (Datum)                       
url     URLField      url                                
name    CharField     Name (Nom)                         
======= ============= ===================================

    
Defined in :srcref:`/lino/apps/dsbe/models.py`

Referenced from




.. index::
   single: field;id
   
.. _lino.links.Link.id:

Field **Link.id**
=================





Type: AutoField

   
.. index::
   single: field;user
   
.. _lino.links.Link.user:

Field **Link.user**
===================





Type: ForeignKey

   
.. index::
   single: field;person
   
.. _lino.links.Link.person:

Field **Link.person**
=====================





Type: ForeignKey

   
.. index::
   single: field;company
   
.. _lino.links.Link.company:

Field **Link.company**
======================





Type: ForeignKey

   
.. index::
   single: field;type
   
.. _lino.links.Link.type:

Field **Link.type**
===================





Type: ForeignKey

   
.. index::
   single: field;date
   
.. _lino.links.Link.date:

Field **Link.date**
===================





Type: DateTimeField

   
.. index::
   single: field;url
   
.. _lino.links.Link.url:

Field **Link.url**
==================





Type: URLField

   
.. index::
   single: field;name
   
.. _lino.links.Link.name:

Field **Link.name**
===================





Type: CharField

   


