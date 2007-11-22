## Copyright 2007 Luc Saffre 

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

a simple form mailer to be called by the mod_python Publisher handler.


from lino.modpy.form_mailer import email


"""

import smtplib
from mod_python import apache
# import apache

WEBMASTER = "webmaster"   # webmaster e-mail
SMTP_SERVER = "localhost" # your SMTP server

def email(req, name, email, comment, **kw):

    if not (name and email and comment):
        return "Sorry: name, email and comment are required."

    if kw.has_key('_recipient'):
        recipient=kw["_recipient"]
    else:
        recipient=WEBMASTER
    # create the message text
    msg = """\
From: %s
Subject: form feedback
To: %s


""" % (email, recipient)

    msg += "name: %s\n" % name
    msg += "email: %s\n" % email
    # msg += "URI:%s\n" % req.connection.the_request
    msg += "comment:\n\n %s\n\n" % comment
    
    msg += "other:\n"

    for k,v in kw.items():
        if not k.startswith('_'):
            msg += str(k) + ":" + str(v) + "\n\n"
    
    msg += "\nRequest:\n"
    for k in dir(req):
        if not k.startswith('_'):
            msg += "- " + str(k) + ":" + str(getattr(req,k)) + "\n"
    
    # send it out
    conn = smtplib.SMTP(SMTP_SERVER)
    conn.sendmail(email, [recipient,WEBMASTER], msg)
    conn.quit()

    # provide feedback to the user

    if kw.has_key('_response_ok'):
        req.headers_out['location'] = kw['_response_ok']
        req.status = apache.HTTP_MOVED_TEMPORARILY
        #return apache.OK
        raise apache.SERVER_RETURN, apache.OK
        #return req.internal_redirect(kw['_response_ok'])
    else:
      s = """\
<html>

Dear %s,<br>
Thank you for your feedback.

</html>""" % name

      return s
