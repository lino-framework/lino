========
sessions
========



.. currentmodule:: sessions

Defined in :srcref:`/django/contrib/sessions/models.py`




.. index::
   pair: model; Session
   single: field;session_key
   single: field;session_data
   single: field;expire_date

.. _dsbe.sessions.Session:

-----------------
Model ``Session``
-----------------




    Django provides full support for anonymous sessions. The session
    framework lets you store and retrieve arbitrary data on a
    per-site-visitor basis. It stores data on the server side and
    abstracts the sending and receiving of cookies. Cookies contain a
    session ID -- not the data itself.

    The Django sessions framework is entirely cookie-based. It does
    not fall back to putting session IDs in URLs. This is an intentional
    design decision. Not only does that behavior make URLs ugly, it makes
    your site vulnerable to session-ID theft via the "Referer" header.

    For complete documentation on using Sessions in your code, consult
    the sessions documentation that is shipped with Django (also available
    on the Django Web site).
    
  
============ ============= ==============================================================
name         type          verbose name                                                  
============ ============= ==============================================================
session_key  CharField     session key (Sitzungs-ID,clé de session,sessiesleutel)        
session_data TextField     session data (Sitzungsdaten,données de session,sessiegegevens)
expire_date  DateTimeField expire date (Verfallsdatum,date d'expiration,verloopdatum)    
============ ============= ==============================================================

    
Defined in :srcref:`/django/contrib/sessions/models.py`


