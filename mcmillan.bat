@echo off
rem svn stat -u >> dist.log
rem if errorlevel 1 goto fehler
rem goto weiter
rem :fehler
rem echo (svn stat -u failed) >> dist.log
rem pause
rem :weiter
set oldpath=%PATH%
set PATH=
path %PATH%;c:\python23\Scripts;c:\python23
path %PATH%;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
path %PATH%;t:\data\PATH
rem path %PATH%;u:\cygwin\bin
path %PATH%;s:\svn-1.0.6
python s:\Installer\Build.py lino.spec -o c:\temp\linobuild
path %OLDPATH%
set oldpath=%PATH%
