@echo off
svn info >> dist.log
set oldpath=%PATH%
set PATH=
path %PATH%;c:\python23\Scripts;c:\python23
path %PATH%;C:\WINDOWS\system32;C:\WINDOWS;C:\WINDOWS\System32\Wbem
path %PATH%;t:\data\PATH
python s:\Installer\Build.py lino.spec -o c:\temp\linobuild
path %OLDPATH%
set oldpath=%PATH%
