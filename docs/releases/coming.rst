Coming
======

Bugfixes
--------

- Wenn man z.B. in der Liste der Stellen 
  auf einen Stellenanbieter klickte um dessen Detail zu sehen, 
  kam stattdessen ein Traceback auf dem Server.
  (:doc:`/blog/2012/0305`)
  
- Die "(zeigen)"-Links im Detail Organisation und Person 
  funktionierten nicht. 
  (:doc:`/blog/2012/0305`)

Internal changes
----------------

Administrators need to ``aptitude install python-lxml`` before upgrading.
:mod:`lino.utils.xmlgen` turned out to be a reinvention of the wheel 
and has been replaced by `lxml <http://www.lxml.de>`_.

