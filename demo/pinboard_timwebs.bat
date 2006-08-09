@echo off
call lino sync -r t:\data\luc\privat\tim\web c:\temp\web
python t:\svnwork\lino\trunk\demo\pinboard_timwebs.py --loadMirrorsFrom c:\temp\web\lino
 
