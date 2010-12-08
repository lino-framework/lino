Tabellenreferenz
================


================================= =============================== ========================
Modell                            Deutsch                         Français
================================= =============================== ========================
:class:`dsbe.Contract`            Vertrag                         Contrat
:class:`dsbe.ContractType`        Vertragsart                     Type de contrat
:class:`contacts.ContactType`     Eigenschaft                     rôle
:class:`contacts.Company`         Firma (Betrieb, Organisation)   Organisation
:class:`contacts.Person`          Person                          Personne
:class:`contacts.CompanyType`     Firmenart                       Type d'organisation
================================= =============================== ========================


**Overview**

  A :class:`Contact` is either a :class:`Person` or a :class:`Company`.

  The :class:`Activity` of a :class:`Person` or :class:`Company` 
  indicates in what professional area they are active.

  :class:`Coaching` is when a :class:`auth.User` has been designated responsible 
  for a :class:`Person`. There may be more than one responsible user per person, 
  each one having a different :class:`CoachingType`.

  For each :class:`Person` we have a list of :class:`Exclusions <Exclusion>` 
  (each with an optional :class:`ExclusionType`).

  For each :class:`Person` we keep a record of her :class:`LanguageKnowledge`.
  
  
  ...




.. module:: dsbe


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
    
