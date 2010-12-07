Tabellenreferenz
================




.. module:: dsbe

========================== =============================== ========================
Modell                     Deutsch                         Français
========================== =============================== ========================
:class:`Contract`          Vertrag                         Contrat
:class:`ContractType`      Vertragsart                     Type de contrat
:class:`ContactType`       Eigenschaft                     rôle
:class:`Company`           Firma (Betrieb, Organisation)   Organisation
:class:`Person`            Person                          Personne
:class:`CompanyType`       Firmenart                       Type d'organisation
========================== =============================== ========================


.. class:: ContractType

  .. attribute:: ref
  
    a short "reference" name that should be unique.
    Used in document templates when testing for text blocks specific 
    to a certain contract type.
    
  .. attribute:: name
  
    the string displayed in comboboxes when selecting a ContractType.
    Also used as title in document templates for contracts.
  
  .. attribute:: name_fr
  
    The optional french version of :attr:`name`.
    See :doc:`/topics/babel`.
    
    
.. class:: ContactType

  .. attribute:: name
  
    the string displayed in comboboxes when selecting a ContactType.
    Also used at "in seiner Eigenschaft als ..." in document templates for contracts.
  
  .. attribute:: name_fr
  
    The optional french version of :attr:`name`.
    See :doc:`/topics/babel`.
  
.. class:: CompanyType

  .. attribute:: name
  
    the string displayed in comboboxes when selecting a CompanyType.
  
  .. attribute:: contract_type
    
      The default ContractType to apply on contracts with a company of this CompanyType.

