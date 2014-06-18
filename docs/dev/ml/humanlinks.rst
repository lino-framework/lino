Human Links
===========

.. module:: ml.humanlinks

Adds Links beween persons.

.. class:: LinkTypes

    List of possible choices for the `Type` field of a
    :ddref:`humanlinks.Link`. The default demo fixture loads the
    following data:
    
    .. django2rst::
        
        settings.SITE.login('robin').show(humanlinks.LinkTypes)



.. class:: Link

    A link between two persons.

.. class:: LinksByHuman

    Display all human links of the master, using both the parent and
    the child directions.

    It is a cool usage example for using a
    :meth:`dd.Table.get_request_queryset` method instead of
    :attr:`dd.Table.master_key`.

    It is also a cool usage example for the
    :meth:`dd.Tableget_slave_summary` method.




