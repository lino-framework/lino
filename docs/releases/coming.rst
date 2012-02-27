Coming
======

This is a mere bugfix release:

- Bug bei Eingabe eines jobs.Contract: 
  wenn Firma mehr als einen Ansprechpartner hatte,
  setzte er in full_clean das "Vertreten durch" 
  immer auf leer. Die Schnelllösung war nur ein Flicken, 
  denn mit der setzte er "Vertreten durch" *nicht* auf leer, 
  wenn die Organisation nicht mit der der Kontaktperson 
  übereinstimmte (also die Organisation geändert worden war 
  und "Vertreten durch" noch auf dem alten Wert stand.
  
- Some more little bugs discovered internally :doc:`/blog/2012/0227`.


Database migration required:
:func:`lino.apps.dsbe.migrate.migrate_from_1_4_2`