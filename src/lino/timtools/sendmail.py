raise "no longer used. now in scripts/sendmail.py"

"""\
sendmail sends an email stored in a file to a list of recipients
stored in a separate list file.

SYNTAX :
  sendmail [options] FILE

  where FILE is the input file (can be text or html)
  
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

See sendmail.txt for more information.
"""

from lino import __version__


import smtplib
import string
import socket
import sys
import os.path
import getopt
import getpass
import glob
import email
import email.Utils
import mimetypes



class SendMail:

	def __init__(self,argv):
		print argv
		# print COPYRIGHT
		try:
			opts, args = getopt.getopt(argv,
												"d?h:s:u:p:r:",
												["debug",
												 "help",
												 "sender=",
												 "host=",
												 "user=",
												 "password=",
												 "recipient="])

		except getopt.GetoptError,e:
			print __doc__
			sys.exit(-1)

		if len(args) == 0:
			print __doc__
			sys.exit(-1)

		self.sender = None
		self.recipient = None
		self.server = None
		self.debug = False
		self.dataDir = '.'
		self.user = None
				
		for o, a in opts:
			if o in ("-?", "--help"):
				usage()
				sys.exit()
			elif o in ("-d", "--debug"):
				self.debug = True
			elif o in ("-s", "--sender"):
				self.sender = a
			elif o in ("-r", "--recipient"):
				self.recipient = a
			elif o in ("-h", "--host"):
				self.host = a
			elif o in ("-u", "--user"):
				self.user = a
			elif o in ("-p", "--password"):
				self.password = a

		for o in ("host",): # ,"user"):
			if not hasattr(self,o):
				raise "--%s : must be specified" % o

		if not self.connect():
			raise "Abort : connect() failed"

		
		self.count_ok = 0
		self.count_nok = 0

		for pattern in args:
			l = glob.glob(pattern)
			if len(l) > 0:
				self.ToUserLog("Sending %d messages." % len(l))
				for filename in l:
					self.processFile(filename)

		self.server.quit()
		
		self.ToUserLog("Sent %d messages." % self.count_ok)
		if self.count_nok != 0:
			self.ToUserLog("(%d failures)" % self.count_nok)

		
	def connect(self):

		try:
			self.server = smtplib.SMTP(self.host)
		except socket.gaierror,e:
			self.ToUserLog("Could not connect to %s" % self.host)
			self.ToUserLog(str(e))
			return False

		# server.set_debuglevel(1)

		if self.user is None:
			self.ToUserLog("Using anonymous SMTP")
			return True

		if not hasattr(self,"password"):
			self.password = getpass.getpass(
				'Password for %s at %s : ' % (self.user,self.host))
			
		try:
			self.server.login(self.user,self.password)
			return True
		
		except smtplib.SMTPHeloError,e:
			self.ToUserLog("The server didn't reply properly to the 'HELO' greeting.")
			self.ToUserLog(str(e))
		except smtplib.SMTPAuthenticationError,e:
			self.ToUserLog("The server didn't accept the username/password combination.")
			self.ToUserLog(str(e))
		except smtplib.SMTPException,e:
			#self.ToUserLog("No suitable authentication method was found.")
			self.ToUserLog(str(e))
			
		return False

	def processFile(self,filename):
		self.ToUserLog(filename)
		self.dataDir = os.path.dirname(filename)
		if len(self.dataDir) == 0:
			self.dataDir = "."

		(root,ext) = os.path.splitext(filename)
		
		ctype, encoding = mimetypes.guess_type(filename)
		if ctype is None:
			self.ToUserLog("ignored file %s : could not guess mimetype"
								% s)
			return
		maintype, subtype = ctype.split('/', 1)
		if maintype == "image": 
			from email.MIMEImage import MIMEImage
			from email.MIMEBase import MIMEBase
			msg = MIMEBase("multipart", "mixed")
			if False:
				msg['Subject'] = filename
			else:
				msg['Subject'] = "noconfirm"

				""" When you add photos to your account as email
				 attachments, you can specify that you don't want to
				 receive a confirmation email from us.	 In the subject
				 line of the email that you send us, type noconfirm You
				 won't receive any confirmation messages when we receive
				 these photos.	 """

			#msg.epilogue = ""
			#msg.preamble = ""

			
			
##				dummyTextMessage = email.message_from_string("\n")
##				dummyTextMessage.add_header('Content-Type',
##													 'text/plain',
##													 charset='us-ascii',
##													 format='flowed')
##				dummyTextMessage.add_header('Content-Transfer-Encoding',
##													 '7bit')
##				msg.attach(dummyTextMessage)
			
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

		if self.recipient is None:
			addrlist = open("%s/addrlist.txt" % self.dataDir)

			for toAddr in addrlist.xreadlines():
				if toAddr and not toAddr[0] == "#":
					toAddr = toAddr.strip()
					if len(toAddr) != 0:
						self.sendto(msg,toAddr)

		else:
			# msg["To"] = self.recipient
			self.sendto(msg,self.recipient)
					


	def sendto(self,msg,toAddr):

		# note : simply setting a header does not overwrite an existing
		# header with the same key! 

		del msg["To"] 
		msg["To"] = toAddr
		
		if not msg.has_key("Subject"):
			raise "Subject header is missing"
		if not msg.has_key("Date"):
			msg["Date"] = email.Utils.formatdate(None,True)


		if self.sender is None:
			sender = msg['From'].encode('latin1')
		else:
			sender = self.sender
			del msg["From"] 
			msg["From"] = self.sender
			
		# body = str(msg)
		body = msg.as_string(unixfrom=0)
		try:
			self.server.sendmail(sender, (toAddr,), body)
			# self.ToUserLog("%s : ok" % toAddr)
			self.ToUserLog("Sent '%s' at %s to %s" % (msg["Subject"],
																 msg["Date"],
																 toAddr))
			self.count_ok += 1
			if self.debug:
				self.ToUserLog("=" * 80 + "\n"
									+ body + "\n"
									+ "=" * 80)
			return 
		
		except smtplib.SMTPRecipientsRefused,e:
			self.ToUserLog("%s : %s" % (toAddr,str(e)))
			# All recipients were refused. Nobody got the mail.
		except smtplib.SMTPHeloError,e:
			self.ToUserLog("%s : %s" % (toAddr,str(e)))
		except smtplib.SMTPSenderRefused,e:
			self.ToUserLog("%s : %s" % (toAddr,str(e)))
		except smtplib.SMTPDataError,e:
			self.ToUserLog("%s : %s" % (toAddr,str(e)))
			
		self.count_nok += 1
		return 

	def ToUserLog(self,msg):
		try:
			f = open("%s/user.log" % self.dataDir,"a")
			f.write(str(msg)+"\n")
			print msg
		except IOError:
			print "[no logfile] " + msg



			
 
if __name__ == "__main__":
	from lino.misc import gpl
	print "sendmail version " + __version__ 
	print gpl.copyright('2002-2003','Luc Saffre')
	SendMail(sys.argv[1:])

		
