@echo off
set VER=0.1.0
set DISTDIR=c:\temp\linodist
set WWWDIR=t:\data\luc\www\lsaffre\comp\dl\lino

if not exist %DISTDIR%\*.* goto error
del %DISTDIR%\*.*

if exist %WWWDIR%\lino-%VER%.zip goto error1
if exist %WWWDIR%\linosrc-%VER%.zip goto error1

python s:\Installer\Build.py prn2pdf.spec -o build
python s:\Installer\Build.py sendmail.spec -o build
python s:\Installer\Build.py pds2pdf.spec -o build
echo PRESS NOW CTRL-C IF THE BUILD FAILED
pause

rem linosrc.zip :
echo Writing %WWWDIR%\linosrc-%VER%.zip...
zip -r %WWWDIR%\linosrc-%VER%.zip CHANGES COPYING *.py *.BAT *.spec

rem lino.zip
xcopy COPYING %DISTDIR% /v
c:
cd %DISTDIR%
echo Writing %WWWDIR%\lino-%VER%.zip...
zip %WWWDIR%\lino-%VER%.zip *.*
t:
goto ende


:error1
echo Error : Pilatus problem. One of the output files...
echo %WWWDIR%\lino-%VER%.zip 
echo %WWWDIR%\linosrc-%VER%.zip 
echo ... exists. Please delete it yourself.


:error
echo Some error occured

:ende
