## Copyright 2002-2007 Luc Saffre

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

"""\
mandatory options :
  -s, --sender     sender's Name and email
  -h, --host       name of SMTP host
  
optional options :  
  -u, --user        sender's login name
                    (anonymous access if omitted)
  -r, --recipient   recipient's Name and email
                    (taken from addrlist.txt if not given)                   
  -p, --password    sender's login password
                    (asked interactively if not given)
  -d, --debug       turn debug mode on
  -h, --help        display this text

"""

from lino.console.application import Application, \
     UsageError, OperationFailed # , ApplicationError

#from lino.ui.console import ConsoleApplication, \
#     UsageError, ApplicationError
#from lino import __version__


import smtplib
#import string
import socket
import sys
import os.path
opj=os.path.join
#import getopt
import getpass
import glob
import email
import email.Utils
import mimetypes


from email import encoders
from email.message import Message
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText




class Sendmail(Application):
    
    name="Lino/sendmail"
    copyright="""\
Copyright (c) 2002-2007 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url="http://lino.saffre-rumma.ee/sendmail.html"
    
    usage="usage: lino sendmail [options] FILE"
    
    description="""\
sends an email stored in a FILE to a list of recipients
stored in a separate list file.
FILE is the input file (can be text or html).
"""
    
    def setupOptionParser(self,parser):
        #self.attach_files = []
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-s", "--subject",
                          help="the Subjet: line of the mail",
                          action="store",
                          type="string",
                          dest="subject",
                          default=None)
    
##         parser.add_option("-a", "--attach",
##                           help="add the specified FILE to the mail as attachment",
##                           action="callback",
##                           callback=self.attachfile,
##                           type="string",
##                           default=None)
    
        parser.add_option("-f", "--from",
                          help="the From: line (sender) of the mail",
                          action="store",
                          type="string",
                          dest="sender",
                          default=None)
    
        parser.add_option("-t", "--to",
                          help="""
The To: line (recipient) of the mail.
Taken from addrlist.txt if not given.
""",
                          action="store",
                          type="string",
                          dest="recipient",
                          default=None)
    
        parser.add_option("-r", "--host",
                          help="the SMTP relay host",
                          action="store",
                          type="string",
                          dest="host",
                          default=None)
        
        parser.add_option("-u", "--user",
                          help="the username for the SMTP host",
                          action="store",
                          type="string",
                          dest="user",
                          default=None)
    
        parser.add_option("-p", "--passwort",
                          help="the username for the SMTP host",
                          action="store",
                          type="string",
                          dest="password",
                          default=None)

##     def attachfile(self,option, opt, value, parser):
##         self.attach_files.append(value)
    

    def run(self):
        
        if len(self.args) == 0:
            raise UsageError("needs 1 argument")

        self.server = None
        self.dataDir = '.'
        self.count_ok = 0
        self.count_nok = 0


        if self.options.host is None:
            raise UsageError("--host must be specified")

##         for fn in  self.attach_files:
##             if not os.path.exists(fn):
##                 raise OperationFailed("File %s does not exist."%fn)
        
        files=[]
        for pattern in self.args:
            files += glob.glob(pattern)
            
        self.count_todo = len(files)
        if self.count_todo == 0:
            self.notice("Nothing to do: no input files found.")
            return

        # if first input file is .eml, then this becomes the outer message
        if files[0].lower().endswith(".eml"):
            first = email.message_from_file(open(files[0])) 
            if not first.has_key("Content-Type"):
                first["Content-Type"] = "text/plain"
            if not first.has_key("Content-Transfer-Encoding"):
                first["Content-Transfer-Encoding"] = "8bit"
            del files[0]
            self.count_todo -= 1
        else:
             first=None
            
        self.notice("Reading %d input files.",self.count_todo)
        
        if len(files) == 0:
            outer=first
        else:
            # Create the enclosing (outer) message
            outer = MIMEMultipart()
            # outer.preamble = 'You will not see this in a MIME-aware mail reader.\n'
            if first is not None:
                first.add_header('Content-Disposition', 'inline')
                outer.attach(first)
        
        i = 1
        for filename in files:
            self.notice(u"%s (%d/%d)",filename,i,self.count_todo)
            part=self.file2msg(filename)
            # Set the filename parameter
            part.add_header('Content-Disposition', 'attachment',
                           filename=os.path.basename(filename))
            outer.attach(part)
            i += 1

        subject = self.options.subject
        recipient = self.options.recipient
        sender = self.options.sender
            
        for part in outer.walk():
            if subject is None: subject=part["Subject"]
            if sender is None: sender=part["From"]
            if recipient is None: recipient=part["To"]

        outer['Subject'] = subject
        outer['To'] = recipient
        outer['From'] = sender
            
        if recipient is None:
            recipients=[]
            for addr in open(opj(self.dataDir,"addrlist.txt")).xreadlines():
                addr = addr.strip()
                if len(addr) != 0 and addr[0] != "#":
                    recipients.append(addr)
        else:
            recipients=[recipient]
            
                    
        self.notice("Message size: %d bytes.",len(str(outer)))
        self.notice(u"Send this to %d recipients: %s",len(recipients),", ".join(recipients))
        
        if not self.confirm("Okay?"):
            return
        
        self.connect()

        for r in recipients:
            self.sendto(outer,r)
        
##         if self.options.recipient is None:
##             if outer["To"] is None:
##                 addrlist = open(opj(self.dataDir,"addrlist.txt"))

##                 for toAddr in addrlist.xreadlines():
##                     toAddr = toAddr.strip()
##                     if len(toAddr) != 0 and toAddr[0] != "#":
##                         self.sendto(outer,toAddr)
##             else:
##                 self.sendto(outer,outer["To"])
##         else:
##             # msg["To"] = self.recipient
##             self.sendto(outer,self.options.recipient)
            
        self.server.quit()
        
        self.notice("Sent %d messages.", self.count_ok)
        if self.count_nok != 0:
            sess.notice("(%d failures)",self.count_nok)

        
    def file2msg(self,filename):
        if not os.path.exists(filename):
            raise OperationFailed(u"File %s does not exist." % filename)
        self.dataDir = os.path.dirname(filename)
        if len(self.dataDir) == 0:
            self.dataDir = "."
            
        (root,ext) = os.path.splitext(filename)

        ctype, encoding = mimetypes.guess_type(filename)

        if ctype is None or encoding is not None:
            # No guess could be made, or the file is encoded (compressed), so
            # use a generic bag-of-bits type.
            ctype = 'application/octet-stream'
        
        maintype, subtype = ctype.split('/', 1)

        if maintype == 'text':
            fp = open(filename)
            # Note: we should handle calculating the charset
            msg = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'image':
            fp = open(filename, 'rb')
            msg = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
        elif maintype == 'audio':
            fp = open(filename, 'rb')
            msg = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
        else:
            fp = open(filename, 'rb')
            msg = MIMEBase(maintype, subtype)
            msg.set_payload(fp.read())
            fp.close()
            # Encode the payload using Base64
            encoders.encode_base64(msg)

        return msg




        

    def _file2msg(self,filename,i):
        self.notice("%s (%d/%d)",filename,i,self.count_todo)
        self.dataDir = os.path.dirname(filename)
        if len(self.dataDir) == 0:
            self.dataDir = "."

        (root,ext) = os.path.splitext(filename)

        
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None:
            self.warning(
                "ignored file %s : could not guess mimetype", s)
            return
        
        maintype, subtype = ctype.split('/', 1)
        if maintype == "image": 
            from email.MIMEImage import MIMEImage
            from email.MIMEBase import MIMEBase
            msg = MIMEBase("multipart", "mixed")
            if self.options.subject is None:
                msg['Subject'] = ("%s (%d/%d)" % (filename,i,
                                                  self.count_todo))
            else:
                msg['Subject'] = self.options.subject

                """ epson.com : When you add photos to your account as
                 email attachments, you can specify that you don't want to
                 receive a confirmation email from us.  In the subject
                 line of the email that you send us, type noconfirm You
                 won't receive any confirmation messages when we receive
                 these photos.  """

            #msg.epilogue = ""
            #msg.preamble = ""

            
            
##              dummyTextMessage = email.message_from_string("\n")
##              dummyTextMessage.add_header('Content-Type',
##                                                   'text/plain',
##                                                   charset='us-ascii',
##                                                   format='flowed')
##              dummyTextMessage.add_header('Content-Transfer-Encoding',
##                                                   '7bit')
##              msg.attach(dummyTextMessage)
            
            fp = open(filename, 'rb')
            try:
                # subtype = ext[1:]
                img = MIMEImage(fp.read(),subtype,name=filename)
                img.add_header('Content-Disposition',
                               'inline',
                               filename=filename)
            except TypeError,e:
                # Could not guess image MIME subtype
                raise
            fp.close()
            msg.attach(img)

            
        else:
            # f = ConvertReader(filename,in_enc="cp437",out_enc="latin1")
            # msg = email.message_from_file(f) 
            msg = email.message_from_file(open(filename)) 
            if not msg.has_key("Content-Type"):
                msg["Content-Type"] = "text/plain"
            if not msg.has_key("Content-Transfer-Encoding"):
                msg["Content-Transfer-Encoding"] = "8bit"
            if len(self.attach_files) > 0:
                mainmsg = MIMEMultipart()
                #mainmsg = email.mime.multipart.MIMEMultipart()
                if self.options.subject is None:
                    mainmsg['Subject'] = msg["Subject"]
                else:
                    mainmsg['Subject'] = self.options.subject
                mainmsg['To'] = msg["To"]
                mainmsg['Cc'] = msg["Cc"]
                mainmsg['Bcc'] = msg["Bcc"]
                #mainmsg['Date'] = msg["Date"]
                msg.add_header('Content-Disposition','inline')
                mainmsg.attach(msg)
                msg=mainmsg
                for fn in self.attach_files:
                    att=email.message_from_file(open(fn))
                    ctype, encoding = mimetypes.guess_type(fn)
                    print ctype, encoding
                    att.add_header('Content-Type',ctype)
                    att.add_header('Content-Transfer-Encoding',encoding)
                    att.add_header('Content-Disposition','attachment',filename=fn)
                    msg.attach(att)
            
        #print "Date: ", msg["Date"]
        #print "Subject: ", msg["Subject"]
        #print "From: ", msg["From"]

        # self.beginLog(root+".log")

        return msg

            
        # self.endLog()
                    

    def connect(self):

        try:
            self.notice("Connecting to %s",self.options.host)
            self.server = smtplib.SMTP(self.options.host)
        except socket.error,e:
            raise OperationFailed(
                "Could not connect to %s : %s" % (
                self.options.host,e))
        except socket.gaierror,e:
            raise OperationFailed(
                "Could not connect to %s : %s" % (
                self.options.host,e))

        # server.set_debuglevel(1)

        if self.options.user is None:
            self.notice("Using anonymous SMTP")
            return 

        if self.options.password is None:
            self.options.password = getpass.getpass(
                'Password for %s@%s : ' % (self.options.user,
                                           self.options.host))
            
        try:
            self.server.login(self.options.user,self.options.password)
            return
        
        except Exception,e:
            raise OperationFailed(str(e))
        
##         except smtplib.SMTPHeloError,e:
##             self.ui.error(
##                 "The server didn't reply properly to the 'HELO' greeting: %s", e)
##         except smtplib.SMTPAuthenticationError,e:
##             self.ui.error(
##                 "The server didn't accept the username/password combination: %s",e)
##         except smtplib.SMTPException,e:
##             self.ui.error(str(e))
##         return False


    def sendto(self,msg,toAddr):

        # note : simply setting a header does not overwrite an existing
        # header with the same key! 

        del msg["To"] 
        msg["To"] = toAddr
        
        if not msg.has_key("Subject"):
            raise "Subject header is missing"
        if not msg.has_key("Date"):
            msg["Date"] = email.Utils.formatdate(None,True)


        if self.options.sender is None:
            sender = msg['From'].encode('latin1')
        else:
            sender = self.options.sender
            del msg["From"] 
            msg["From"] = self.options.sender
            
        # body = str(msg)
        body = msg.as_string(unixfrom=0)
        try:
            self.server.sendmail(sender, (toAddr,), body)
            # self.ToUserLog("%s : ok" % toAddr)
            self.notice(
                u"Sent '%s' at %s to %s",
                msg["Subject"], msg["Date"], toAddr)
            self.count_ok += 1
            self.debug("=" * 80)
            self.debug(body)
            self.debug("=" * 80)
            return 
        
        except smtplib.SMTPRecipientsRefused,e:
            self.error("%s : %s", toAddr,e)
            # All recipients were refused. Nobody got the mail.
        except smtplib.SMTPHeloError,e:
            self.error("%s : %s", toAddr,e)
        except smtplib.SMTPServerDisconnected,e:
            self.error("%s : %s", toAddr,e)
        except smtplib.SMTPSenderRefused,e:
            self.error("%s : %s", toAddr,e)
        except smtplib.SMTPDataError,e:
            self.error("%s : %s", toAddr,e)
            
        self.count_nok += 1
        return 

##  def ToUserLog(self,msg):
##      try:
##          f = open("%s/user.log" % self.dataDir,"a")
##          f.write(str(msg)+"\n")
##          print msg
##      except IOError:
##          print "[no logfile] " + msg


def main(*args,**kw):
    Sendmail().main(*args,**kw)

if __name__ == '__main__':
    main()

        
