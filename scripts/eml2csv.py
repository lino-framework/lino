#----------------------------------------------------------------------
# ID:        $Id: eml2csv.py,v 1.2 2004/03/14 21:58:30 lsaffre Exp $
# Copyright: (c) 2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""\
Usage : eml2csv [options] DIR [DIR...]

eml2csv converts the *.eml files in DIR to a CSV file.

Options:
  
  -o FILE, --output FILE   output to file FILE instead of stdout
  -a, --append             append to existing FILE instead of overwrite
  -c, --cleanup            delete *.eml files after conversion
  -h, --help               display this text
"""

import sys, getopt, os
from email import message_from_file
import csv

from lino import copyright
#from lino.misc import gpl
#from lino import __version__

messageFields = ('date','subject','from','to')
bodyFieldSplitter = '->'
bodyFields = ('select', 'Name', 'Vorname', 'Jahr', 'Sex', 'club_schule', 'Adresse', 'Email', 'land', 'textarea', 'Submit')

def main(dirname,out,cleanUp,verbose):
	#writer = csv.writer(f)
	headers = messageFields+bodyFields
	writer = csv.DictWriter(out,headers) #, extrasaction='ignore')
	# writer.writerow(headers)
	for root, dirs, files in os.walk('.'):
		for fn in files:
			(name,ext) = os.path.splitext(fn)
			if ext.lower() == ".eml":
				fn = os.path.join(root,fn)
				if verbose:
					print fn
				input = file(fn,"r")
				eml2csv(input,writer)
				input.close()
				if cleanUp:
					os.remove(fn)

def eml2csv(input,writer):
	msg = message_from_file(input)
	for part in msg.walk():
		if not part.is_multipart():
			d = body2dict(part.get_payload())
			#print d
			for n in messageFields:
				d[n] = part.get(n)
			writer.writerow(d)


def body2dict(body):
	d = {}
	for line in body.splitlines():
		if len(line.strip()) == 0:
			pass
		else:
			a = line.split(bodyFieldSplitter)
			if len(a) == 2:
				fldName = a[0].strip() #.lower()
				#print "d[%s] = %s" % (repr(fldName),repr(a[1].strip()))
				if fldName in bodyFields:
					d[fldName] = a[1].strip()
				else:
					raise "Bad field name %s" % fldName
			else:
				raise "invalid content: " + line
	return d
	



	
if __name__ == '__main__':
	print "lino eml2csv" # version " + __version__
	print copyright('2004','Luc Saffre')

	try:
		opts, args = getopt.getopt(sys.argv[1:],
											"?ho:",
											["help", "output="])

	except getopt.GetoptError,e:
		print __doc__
		print e
		sys.exit(-1)

	outputfile = None
	cleanUp = False
	verbose = False
	append = False
	
	
	for o, a in opts:
		if o in ("-?", "-h", "--help"):
			print __doc__
			sys.exit()
		elif o in ("-o", "--output"):
			outputfile = a
		elif o in ("-v", "--verbose"):
			verbose = True
		elif o in ("-a", "--append"):
			append = True
		elif o in ("-c", "--cleanUp"):
			cleanUp = True

	if outputfile is not None:
		if os.path.exists(outputfile):
			if append:
				f = file(outputfile,"a")
			else:
				f = file(outputfile,"w")
		else:
			f = file(outputfile,"w")
	else:
		f = sys.stdout
			
			
	if len(args) == 0:
		args = ['.']

	for dirname in args:
		main(dirname,f,cleanUp,verbose)
