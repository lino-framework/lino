@echo off
s:
cd \phpdoc-1.1.0rc2
s:\php\php-cli.exe phpdoc -t c:/temp/lino-api -o HTML:default:default -f t:/data/luc/www/phptest/lino/*.php
go lino
