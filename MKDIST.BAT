@echo off
set oldpath=%PATH%
set PATH=
path %PATH%;c:\python23\Scripts;c:\python23
rem PATH %PATH%;u:\CYGWIN\BIN
path %PATH%;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
path %PATH%;t:\data\PATH
path %PATH%;s:\blink\BIN;s:\clip52e\bin;s:\harbour\bin
rem path %PATH%;u:\CYGWIN\USR\BIN;u:\CYGWIN\USR\LOCAL\BIN
path %PATH%;s:\texmf\miktex\bin;s:\mysql\bin;s:\emacs\bin;s:\gnuserv
path
pause
python s:\Installer\Build.py lino.spec -o c:\temp\linobuild
path %OLDPATH%
set oldpath=%PATH%
