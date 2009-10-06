import os,sys

UserAbort = "aborted by user"


def Confirm(msg,default="y"):
   s = raw_input(msg)
   if s == "":
      s = default
   else:
      s = s.lower()
  
   if s != "y":
      raise UserAbort


renameList = []
compareList = []

def collect(path):
   for fn in os.listdir(path):
      pfn = os.path.join(path,fn)
      if os.path.isdir(pfn):
         collect(pfn)
      else:
         if fn != fn.lower():
            #print "%s -> %s" % (fn, fn.lower())
            renameList.append( (pfn,
                              os.path.join(path,fn.lower())
                              ))
            compareList.append(pfn)


collect(".")

#if len(renameList) == 0: sys.exit(0)

Confirm("Okay to rename %d files [Yn]?" % len(renameList))
for (old,new) in renameList:
   os.rename(old,new)
print "%d files renamed" % len(renameList)



Confirm("Okay to compare %d files [Yn]?" % len(compareList)))

ftp = FTP(ftp_address)
ftp.login(ftp_user,ftp_password)


for fn in compareList:

   try:
      sendme = open(fn,'rb')
   except IOError:
			print "* file",i,"did not load. Does it exist?"
			loaderror = 1

		if loaderror == 0:
			try:
				ftp.storbinary('STOR '+i,sendme,8192)
			except all_errors:
				print "* Error sending file",i
			sendme.close()
		


	# Shut down connection

	print "Closing connection to",ftpadress+'...'
	ftp.quit()
	print "Done"

