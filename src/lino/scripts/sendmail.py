## Copyright 2002-2005 Luc Saffre

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

from lino.ui.console import ConsoleApplication, \
     UsageError, ApplicationError
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



class Sendmail(ConsoleApplication):
    
    name="Lino/sendmail"
    years='2002-2005'
    author='Luc Saffre'
    
    usage="usage: lino sendmail [options] FILE"
    
    description="""\
sends an email stored in a FILE to a list of recipients
stored in a separate list file.
FILE is the input file (can be text or html).
"""
    
    def setupOptionParser(self,parser):
        ConsoleApplication.setupOptionParser(self,parser)
    
        parser.add_option("-s", "--subject",
                          help="the Subjet: line of the mail",
                          action="store",
                          type="string",
                          dest="subject",
                          default=None)
    
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
    

    def run(self,ui):
        if len(self.args) == 0:
            raise UsageError("needs 1 argument")

        self.server = None
        self.dataDir = '.'
        self.count_ok = 0
        self.count_nok = 0

                

        if self.options.host is None:
            raise UsageError("--host must be specified")

        self.connect()
        
        for pattern in self.args:
            l = glob.glob(pattern)
            self.count_todo = len(l)
            if self.count_todo > 0:
                i = 1
                self.ui.notice(
                    "Sending %d messages.",self.count_todo)
                for filename in l:
                    self.processFile(filename,i)
                    i += 1

        self.server.quit()
        
        self.ui.notice("Sent %d messages.", self.count_ok)
        if self.count_nok != 0:
            self.ui.notice("(%d failures)",self.count_nok)

        
    def connect(self):

        try:
            self.ui.notice("Connecting to %s",self.options.host)
            self.server = smtplib.SMTP(self.options.host)
        except socket.error,e:
            raise ApplicationError(
                "Could not connect to %s : %s" % (
                self.options.host,e))
        except socket.gaierror,e:
            raise ApplicationError(
                "Could not connect to %s : %s" % (
                self.options.host,e))

        # server.set_debuglevel(1)

        if self.options.user is None:
            self.ui.notice("Using anonymous SMTP")
            return 

        if self.options.password is None:
            self.options.password = getpass.getpass(
                'Password for %s@%s : ' % (self.options.user,
                                           self.options.host))
            
        try:
            self.server.login(self.options.user,self.options.password)
            return
        
        except Exception,e:
            raise ApplicationError(str(e))
        
##         except smtplib.SMTPHeloError,e:
##             self.ui.error(
##                 "The server didn't reply properly to the 'HELO' greeting: %s", e)
##         except smtplib.SMTPAuthenticationError,e:
##             self.ui.error(
##                 "The server didn't accept the username/password combination: %s",e)
##         except smtplib.SMTPException,e:
##             self.ui.error(str(e))
##         return False

    def processFile(self,filename,i):
        self.ui.notice("%s (%d/%d)",filename,i,self.count_todo)
        self.dataDir = os.path.dirname(filename)
        if len(self.dataDir) == 0:
            self.dataDir = "."

        (root,ext) = os.path.splitext(filename)
        
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None:
            self.ui.warning(
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
            
        #print "Date: ", msg["Date"]
        #print "Subject: ", msg["Subject"]
        #print "From: ", msg["From"]

        if self.options.recipient is None:
            addrlist = open(opj(self.dataDir,"addrlist.txt"))

            for toAddr in addrlist.xreadlines():
                toAddr = toAddr.strip()
                if len(toAddr) != 0 and toAddr[0] != "#":
                    self.sendto(msg,toAddr)

        else:
            # msg["To"] = self.recipient
            self.sendto(msg,self.options.recipient)
                    


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
            self.ui.notice(
                "Sent '%s' at %s to %s",
                msg["Subject"], msg["Date"], toAddr)
            self.count_ok += 1
            self.ui.debug("=" * 80)
            self.ui.debug(body)
            self.ui.debug("=" * 80)
            return 
        
        except smtplib.SMTPRecipientsRefused,e:
            self.ui.error("%s : %s", toAddr,e)
            # All recipients were refused. Nobody got the mail.
        except smtplib.SMTPHeloError,e:
            self.ui.error("%s : %s", toAddr,e)
        except smtplib.SMTPServerDisconnected,e:
            self.ui.error("%s : %s", toAddr,e)
        except smtplib.SMTPSenderRefused,e:
            self.ui.error("%s : %s", toAddr,e)
        except smtplib.SMTPDataError,e:
            self.ui.error("%s : %s", toAddr,e)
            
        self.count_nok += 1
        return 

##  def ToUserLog(self,msg):
##      try:
##          f = open("%s/user.log" % self.dataDir,"a")
##          f.write(str(msg)+"\n")
##          print msg
##      except IOError:
##          print "[no logfile] " + msg



consoleApplicationClass = Sendmail

if __name__ == '__main__':
    consoleApplicationClass().main() # console,sys.argv[1:])
            
 
## if __name__ == "__main__":
##  print "sendmail" # version " + __version__ 
##  from lino import copyright
##  print copyright('2002-2004','Luc Saffre')
##  SendMail(sys.argv[1:])

        
