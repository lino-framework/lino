GPDN - General Public Database Network
======================================

Das GPDN ist eine meiner Ideen, die momentan als utopisch zu 
bezeichnen ist. Aber Leute wie ich lassen sich ja nicht so 
leicht vom Träumen abhalten, schon gar nicht durch banale 
Bedenken wie Machbarkeit oder Wirtschaftlichkeit...

Der Ausgangspunkt ist: es gibt gewisse Daten, die eigentlich 
Allgemeingut sein sollten. 
Zum Beispiel die Listen aller Länder, Städte und Dörfer 
der Erde, die Liste aller Sprachen... um nur einige zu nennen. 
Solche Daten sollten eigentlich durch eine weltweite unabhängige 
Organisation gepflegt und für alle verfügbar gemacht werden.

Die Wikipedia ist ja so ein zentraler Ort, z.B. haben wir dort die
wohl am besten gepflegte freie `Liste der Staaten der Erde
<http://de.wikipedia.org/wiki/Liste_der_Staaten_der_Erde>`_.

Bestehende Lösungsansätze

- http://www.geonames.org/export/

Aber anders als bei der Wikipedia müssten solche Daten klarer 
strukturiert sein, um auch maschinell leichter 
verarbeitet werden zu können.

Seit kurzem gibt es die `Gemeinsame Normdatei
<http://de.wikipedia.org/wiki/Gemeinsame_Normdatei>`_

Für Länder, Sprachen, Währungen
gibt es wahrscheinlich einigermaßen
freie und brauchbare Listen, die einigermaßen gepflegt sind.

In Lino finden wir einen Ansatz zu einer Lösung in diversen `fixtures`:

- :srcref:`/lino/modlib/countries/fixtures/all_countries.py`
  and :srcref:`/lino/modlib/countries/fixtures/countries.xml`
- :srcref:`/lino/modlib/countries/fixtures/all_languages.py`
  and :srcref:`/lino/modlib/countries/fixtures/iso-639-3_20100707.tab`
- :srcref:`/lino/modlib/countries/fixtures/be.py`
- :mod:`lino.modlib.countries.fixtures.ee`,
  :mod:`lino.modlib.countries.fixtures.est`
  and :srcref:`/lino/modlib/countries/fixtures/sihtnumbrid.csv`


20120331 : Nicht nur Länder und Sprachen, sondern auch Firmen könnten
in so einer Datenbank stehen.  Ein öffentliches internationales
Branchenverzeichnis, das für die dort aufgelisteten Firmen
idealerweise kostenlos sein müsste, weil wir sonst kaum Chancen haben,
einigermaßen komplett zu werden. Die Firmen müssten lediglich
einverstanden sein, dass sie dort stehen und eventuell mithelfen, dass
die Angaben korrekt sind.  So wie `hier
<http://www.grenzecho.net/ArtikelLoad.aspx?aid=45E57E0F-980C-4A7B-86C1-D77C7BAA7369&mode=all>`_
beschrieben sollten wir es natürlich nicht machen...


