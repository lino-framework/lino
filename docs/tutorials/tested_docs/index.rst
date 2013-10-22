.. _tested_docs:


Tested documents
================

.. include:: /include/wip.rst

The :meth:`login <lino.lino_site.Site.login>` method doesn't require any 
password because when somebody has command-line access we trust 
that she has already authenticated. It returns a 
:class:`BaseRequest <lino.core.requests.BaseRequest>` object which 
has a :meth:`show <lino.core.requests.BaseRequest.show>` method.
