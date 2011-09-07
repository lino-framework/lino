=====
users
=====



.. currentmodule:: users

Defined in :srcref:`/lino/modlib/users/models.py`



.. contents:: Table of Contents



.. index::
   pair: model; User

.. _lino.users.User:

--------------
Model **User**
--------------




Represents a User of this site.

This version of the Users table is used on Lino sites with
:doc:`/topics/http_auth`. 

Only username is required. Other fields are optional.

There is no password field since Lino is not responsible for authentication.
New users are automatically created in this table when 
Lino gets a first request with a username that doesn't yet exist.
It is up to the local system administrator to manually fill then 
fields like first_name, last_name, email, access rights for the new user.    

  
============= ============= =============================================================================
name          type          verbose name                                                                 
============= ============= =============================================================================
id            AutoField     ID                                                                           
country       ForeignKey    Country (Land,Pays)                                                          
city          ForeignKey    City (Stadt)                                                                 
name          CharField     Name (Nom)                                                                   
addr1         CharField     Address line before street (Adresszeile vor Straße,Ligne avant le nom de rue)
street_prefix CharField     Street prefix (Präfix Straße,Préfixe rue)                                    
street        CharField     Street (Straße,Rue)                                                          
street_no     CharField     No. (Nr.,N°)                                                                 
street_box    CharField     Box (boîte)                                                                  
addr2         CharField     Address line after street (Adresszeile nach Straße,Ligne après le nom de rue)
zip_code      CharField     Zip code (Postleitzahl,Code postal)                                          
region        CharField     Region (Région)                                                              
language      LanguageField Language (Sprache,Langue)                                                    
email         EmailField    E-Mail (E-mail)                                                              
url           URLField      URL                                                                          
phone         CharField     Phone (Telefon,Téléphone)                                                    
gsm           CharField     GSM                                                                          
fax           CharField     Fax                                                                          
remarks       TextField     Remarks (Bemerkungen,Remarques)                                              
contact_ptr   OneToOneField Contact (Kontakt)                                                            
first_name    CharField     First name                                                                   
last_name     CharField     Last name                                                                    
title         CharField     Title                                                                        
sex           CharField     Sex                                                                          
username      CharField     username                                                                     
is_staff      BooleanField  is staff                                                                     
is_expert     BooleanField  is expert                                                                    
is_active     BooleanField  is active (aktiv,est actif)                                                  
is_superuser  BooleanField  is superuser                                                                 
last_login    DateTimeField last login                                                                   
date_joined   DateTimeField date joined                                                                  
============= ============= =============================================================================

    
Defined in :srcref:`/lino/modlib/users/models.py`

Referenced from
`lino.mails.OutMail.user`_, `lino.jobs.Contract.user`_, `lino.jobs.Contract.user_asd`_, `lino.links.Link.user`_, `lino.contacts.Person.coach1`_, `lino.contacts.Person.coach2`_, `lino.dsbe.PersonSearch.user`_, `lino.dsbe.PersonSearch.coached_by`_, `lino.notes.Note.user`_, `lino.lino.TextFieldTemplate.user`_, `lino.isip.Contract.user`_, `lino.isip.Contract.user_asd`_, `lino.uploads.Upload.user`_, `lino.cal.Calendar.user`_, `lino.cal.Event.user`_, `lino.cal.Task.user`_



.. index::
   single: field;id
   
.. _lino.users.User.id:

Field **User.id**
=================





Type: AutoField

   
.. index::
   single: field;country
   
.. _lino.users.User.country:

Field **User.country**
======================





Type: ForeignKey

   
.. index::
   single: field;city
   
.. _lino.users.User.city:

Field **User.city**
===================





Type: ForeignKey

   
.. index::
   single: field;name
   
.. _lino.users.User.name:

Field **User.name**
===================





Type: CharField

   
.. index::
   single: field;addr1
   
.. _lino.users.User.addr1:

Field **User.addr1**
====================



Address line before street

Type: CharField

   
.. index::
   single: field;street_prefix
   
.. _lino.users.User.street_prefix:

Field **User.street_prefix**
============================



Text to print before name of street, but to ignore for sorting.

Type: CharField

   
.. index::
   single: field;street
   
.. _lino.users.User.street:

Field **User.street**
=====================



Name of street. Without house number.

Type: CharField

   
.. index::
   single: field;street_no
   
.. _lino.users.User.street_no:

Field **User.street_no**
========================



House number

Type: CharField

   
.. index::
   single: field;street_box
   
.. _lino.users.User.street_box:

Field **User.street_box**
=========================



Text to print after :attr:`steet_no` on the same line

Type: CharField

   
.. index::
   single: field;addr2
   
.. _lino.users.User.addr2:

Field **User.addr2**
====================



Address line to print below street line

Type: CharField

   
.. index::
   single: field;zip_code
   
.. _lino.users.User.zip_code:

Field **User.zip_code**
=======================





Type: CharField

   
.. index::
   single: field;region
   
.. _lino.users.User.region:

Field **User.region**
=====================





Type: CharField

   
.. index::
   single: field;language
   
.. _lino.users.User.language:

Field **User.language**
=======================





Type: LanguageField

   
.. index::
   single: field;email
   
.. _lino.users.User.email:

Field **User.email**
====================





Type: EmailField

   
.. index::
   single: field;url
   
.. _lino.users.User.url:

Field **User.url**
==================





Type: URLField

   
.. index::
   single: field;phone
   
.. _lino.users.User.phone:

Field **User.phone**
====================





Type: CharField

   
.. index::
   single: field;gsm
   
.. _lino.users.User.gsm:

Field **User.gsm**
==================





Type: CharField

   
.. index::
   single: field;fax
   
.. _lino.users.User.fax:

Field **User.fax**
==================





Type: CharField

   
.. index::
   single: field;remarks
   
.. _lino.users.User.remarks:

Field **User.remarks**
======================





Type: TextField

   
.. index::
   single: field;contact_ptr
   
.. _lino.users.User.contact_ptr:

Field **User.contact_ptr**
==========================





Type: OneToOneField

   
.. index::
   single: field;first_name
   
.. _lino.users.User.first_name:

Field **User.first_name**
=========================





Type: CharField

   
.. index::
   single: field;last_name
   
.. _lino.users.User.last_name:

Field **User.last_name**
========================





Type: CharField

   
.. index::
   single: field;title
   
.. _lino.users.User.title:

Field **User.title**
====================





Type: CharField

   
.. index::
   single: field;sex
   
.. _lino.users.User.sex:

Field **User.sex**
==================





Type: CharField

   
.. index::
   single: field;username
   
.. _lino.users.User.username:

Field **User.username**
=======================




        Required. 30 characters or fewer. 
        Letters, numbers and @/./+/-/_ characters
        

Type: CharField

   
.. index::
   single: field;is_staff
   
.. _lino.users.User.is_staff:

Field **User.is_staff**
=======================




        Designates whether the user can log into this admin site.
        

Type: BooleanField

   
.. index::
   single: field;is_expert
   
.. _lino.users.User.is_expert:

Field **User.is_expert**
========================




        Designates whether this user has access to functions that require expert rights.
        

Type: BooleanField

   
.. index::
   single: field;is_active
   
.. _lino.users.User.is_active:

Field **User.is_active**
========================




        Designates whether this user should be treated as active. 
        Unselect this instead of deleting accounts.
        

Type: BooleanField

   
.. index::
   single: field;is_superuser
   
.. _lino.users.User.is_superuser:

Field **User.is_superuser**
===========================




        Designates that this user has all permissions without 
        explicitly assigning them.
        

Type: BooleanField

   
.. index::
   single: field;last_login
   
.. _lino.users.User.last_login:

Field **User.last_login**
=========================





Type: DateTimeField

   
.. index::
   single: field;date_joined
   
.. _lino.users.User.date_joined:

Field **User.date_joined**
==========================





Type: DateTimeField

   


