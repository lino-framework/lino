Summary fields
==============

Example: Client has two date fields `active_from` and `active_until` 
whose value is automatically computed.
They are not virtual fields because we want to sort and filter 
on them, and because their values aren't so very dynamic, they 
are the start and end date of the currently active contract.
:meth:`lino_welfare.modlib.pcsw.Client.get_active_contract`

The application must declare them as summary fields by defining::

  class Client(...):
      ...
      def update_active_fields(self):
          c = self.get_active_contract()
          if c is None:
              self.active_from = self.active_until = None
          else:
              self.active_from = c.applies_from
              self.active_until = c.applies_until


... Und dann muss ich noch irgendwie dafür sorgen, 
dass diese Funktion dann immer automatisch aufgerufen wird, 
wenn ein Vertrag dieses Klienten verändert oder erstellt oder gelöscht wurde. 
Eigentlich sollte das ins lino.core.changes integriert werden. 
Aber Achtung: 

- das Löschen eines Vertrags muss behandelt werden *nachdem* 
  der Vertrag gelöscht wurde, während der Change *vorher* 
  erstellt werden muss.
  
- Wenn das verbindende Feld selber geändert wird 
  (Feld `client` eines Vertrags), 
  dann muss die Funktion auf beiden Klienten 
  (dem alten und dem neuen) aufgerufen werden.

