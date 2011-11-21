Konvertierung TIM nach Lino
===========================

.. currentmodule:: lino.apps.dsbe.models

Die Krankenkassen (Adressen aus ADR mit ADR->Type == 'MUT') 
erscheinen in Lino als :class:`Company`, wobei deren `id` wie folgt ermittelt wird:

  id = val(ADR->IdMut) + 199000
  
Die Partner aus TIM kommen entweder nach :class:`contacts.Company` oder nach :class:`contacts.Person`, 
je nachdem ob deren PAR->NoTva leer ist oder nicht. 
Das jeweilige id entspricht der Partnernummer (PAR->IdPar) aus TIM.

Personen und Firmen mit einem id über 200.000 (und unter 800.000) sind in Lino gemacht worden.

`PAR->Allo` geht nach :attr:`Person.title` oder :attr:`Company.prefix`.
