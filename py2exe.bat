@echo off
set oldpath=%PATH%
set PATH=
path %PATH%;c:\python23\Scripts;c:\python23
path %PATH%;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
path %PATH%;t:\data\PATH
path %PATH%;u:\cygwin\bin
path %PATH%;s:\svn-1.0.6
python py2exe.py py2exe
path %OLDPATH%
set oldpath=%PATH%
