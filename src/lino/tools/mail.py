## Copyright Luc Saffre 2003-2006.

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA

"""

used by :
scripts/openmail.py
tests/etc/1.py

"""
import sys,os

import urllib
import email
import webbrowser

def mailto_url(to=None,subject=None,body=None,cc=None):
    """
    encodes the content as a mailto link as described on
    http://www.faqs.org/rfcs/rfc2368.html
    Examples partly taken from 
    http://selfhtml.teamone.de/html/verweise/email.htm
    """
    #url = "mailto:" + urllib.quote(to.strip())
    url = "mailto:" + urllib.quote(to.strip(),"@,")
    sep = "?"
    if cc:
        url+= sep + "cc=" + urllib.quote(cc,"@,")
        sep = "&"
    if subject:
        url+= sep + "subject=" + urllib.quote(subject,"")
        sep = "&"
    if body:
        # Also note that line breaks in the body of a message MUST be
        # encoded with "%0D%0A". (RFC 2368)
        body="\r\n".join(body.splitlines())
        url+= sep + "body=" + urllib.quote(body,"")
        sep = "&"
    # if not confirm("okay"): return
    return url


## def readmail2(filename):
##  "reads a real RFC2822 file"
##  msg = email.message_from_file(open(filename))
##  if msg.is_multipart():
##      raise "%s contains a multipart message : not supported" % filename
##  return msg

def readmail(filename): 
    """reads a "simplified pseudo-RFC2822" file
    """
    
    from email.Message import Message
    msg = Message()

    text = open(filename).read()
    text = text.decode("cp850")
    text = text.encode("iso-8859-1","replace")

    headersDone = False
    subject = None
    to = None
    body = ""
    for line in text.splitlines():
        if headersDone:
            body += line + "\n"
        else:
            if len(line) == 0:
                headersDone = True
            else:
                (name,value) = line.split(':')
                msg[name] = value.strip()
##              if name.lower() == 'subject':
##                  subject = value.strip()
##              elif name.lower() == 'to':
##                  to = value.strip()
##              else:
##                  raise "%s : invalid header field in line %s" % (
##                      name,repr(line))
    msg.set_payload(body)
    return msg



def openmail(msg):
    url = mailto_url(msg.get('to'),msg.get("subject"),msg.get_payload())
    webbrowser.open(url,new=1)

    
