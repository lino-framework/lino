rem @echo off
set YEAR=2011
if not exist docs\blog\%YEAR%\%1.rst goto error
hg ci -m http://code.google.com/p/lino/source/browse/docs/blog/%YEAR%/%1.rst
goto :ende
:error
echo oops!
echo file does not exist: docs\blog\%YEAR%\%1.rst 

:ende
