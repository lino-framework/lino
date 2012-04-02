Konvertierung TIM nach Lino
===========================

.. currentmodule:: lino.apps.dsbe.models


In der :xfile:`settings.py` gibt es folgende Optionen, 
die für die Synchronisierung von Belang sind::

    def TIM2LINO_LOCAL(alias,obj):
        """Hook for local special treatment on instances that have been imported from TIM.
        """
        return obj
        
    def TIM2LINO_USERNAME(userid):
        if userid == "WRITE": return None
        return userid.lower()
        
        
    def TIM2LINO_IS_IMPORTED_PARTNER(obj):
        "`obj` is either a Person or a Company"
        #~ return obj.id is not None and (obj.id < 200000 or obj.id > 299999)
        return False
        #~ return obj.id is not None and (obj.id > 10 and obj.id < 21)
                  


Die Krankenkassen (Adressen aus ADR mit ADR->Type == 'MUT') 
erscheinen in Lino als :class:`Company`, 
wobei deren `id` wie folgt ermittelt wird:

  id = val(ADR->IdMut) + 199000
  
Die Partner aus TIM kommen entweder nach 
:class:`contacts.Company` oder nach :class:`contacts.Person`, 
je nachdem ob deren PAR->NoTva leer ist oder nicht. 
Das jeweilige id entspricht der Partnernummer (PAR->IdPar) aus TIM.

Personen und Firmen mit einem id über 200.000 
(und unter 800.000) sind *in Lino* erstellt worden.

`PAR->Allo` geht nach :attr:`Person.title` oder :attr:`Company.prefix`.





Die Regeln beim Übernehmen der diversen Flags aus TIM sind:

- `newcomer` : `True` wenn Attribut N in TIM gesetzt ist
- `is_deprecated` : `True` wenn Attribut W in TIM gesetzt ist
- `is_active` : False wenn Partnerart I (ansonsten True)
- `is_cpas` : True wenn Partnerart S
- `is_senior` : True wenn Partnerart A

Hier eine Liste der möglichen Partnerattribute in TIM:

- H : Versteckt
- W : Warnung bei Auswahl
- R : Schreibgeschützt
- 2 : als Nebenpartner ignorieren
- A : Altfall (automatisch)
- E : Eingeschlafener Debitor (automatisch)
- N : Neuzugang
