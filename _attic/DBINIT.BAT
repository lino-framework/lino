rem @echo off
rem each module has an SQL script which creates the tables.

set TMPFILE=temp\dbinit.sql

rem For the SYS module there are 3 scripts:
type dbinit\sys.sql > %TMPFILE%
type dbinit\lang.sql >> %TMPFILE%
type dbinit\nations.sql >> %TMPFILE%

type dbinit\addrbook.sql >> %TMPFILE%
type dbinit\docbook.sql >> %TMPFILE%
type dbinit\community.sql >> %TMPFILE%
type dbinit\sdk.sql >> %TMPFILE%

python pin2sql.py pinboard/*.pin >> %TMPFILE%

mysql %1 < %TMPFILE%
