# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

"""
This is taken from Helio Perroni Filho's answer at
http://stackoverflow.com/questions/328356/extracting-text-from-html-file-using-python/3987802#3987802

I added the extract_summary() function. 

Lino never really used this module. 
It was added and dropped the same day 
for the server-side approach of :doc:`/tickets/44`.
"""

from HTMLParser import HTMLParser
from re import sub
from sys import stderr
from traceback import print_exc

class _DeHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.__text = []

    def handle_data(self, data):
        text = data.strip()
        if len(text) > 0:
            text = sub('[ \t\r\n]+', ' ', text)
            self.__text.append(text + ' ')

    def handle_starttag(self, tag, attrs):
        if tag == 'p':
            self.__text.append('\n\n')
        elif tag == 'br':
            self.__text.append('\n')

    def handle_startendtag(self, tag, attrs):
        if tag == 'br':
            self.__text.append('\n\n')

    def text(self):
        return ''.join(self.__text).strip()


def dehtml(text):
    try:
        parser = _DeHTMLParser()
        parser.feed(text)
        parser.close()
        return parser.text()
    except:
        print_exc(file=stderr)
        return text
        
def extract_summary(text):
    if text.startswith('<'):
        text = dehtml(text)
    a = text.split('\n',1)
    ellipsis = False
    if len(a) > 1:
        ellipsis = True
    ln = text.split('\n',1)[0]
    if len(ln) > 30:
        ln = ln[:30]
        ellipsis = True
    if ellipsis:     
        ln += "..."
    return ln
    


def main():
    text = r'''
        <html>
            <body>
                <b>Project:</b> DeHTML<br>
                <b>Description</b>:<br>
                This small script is intended to allow conversion from HTML markup to 
                plain text.
            </body>
        </html>
    '''
    print(dehtml(text))


if __name__ == '__main__':
    main()