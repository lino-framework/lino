"""
publish prepares a local file tree for publishing to a web server.
- rename all files to lower case
- create thumbnails

USAGE:

there are no command-line parameters.
- cd to the root directory of your local file tree
- timtools publish 

"""

from lino import copyleft

import os,sys

from PIL import Image

from lino.misc.console import confirm
#from lino.misc import gpl
  


images = "images"	 # directory containing original size images
thumbnails = "thumbnails"	# directory containing thumbnails
#thumbnails_size = (128,128)
thumbnails_size = (512,512)

upperFilenames = []
upperDirnames = []

imgFilenames = []
imgExtensions = (".jpg",".png")

def collect_upper(path="."):
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			if fn != fn.lower():
				upperDirnames.append( (pfn, pfn.lower()))
			collect_upper(pfn)
		else:
			if fn != fn.lower():
				i = (os.path.join(path.lower(),fn), pfn.lower())
				print "%s -> %s" % i # (pfn, pfn.lower())
				upperFilenames.append(i)
					
def collect_images(path=".",
						 thumbnailsPath=None):
	for fn in os.listdir(path):
		pfn = os.path.join(path,fn)
		if os.path.isdir(pfn):
			# don't walk into directories whose name is "thumbnails"
			if fn == thumbnails:
				continue
			# if 
			if fn == images:
				collect_images(pfn,os.path.join(path,thumbnails))
			elif thumbnailsPath == None:
				collect_images(pfn)
			else:
				collect_images(pfn,os.path.join(thumbnailsPath,fn))
		else:
			(root,ext) = os.path.splitext(fn)
			if not ext in imgExtensions:
				continue
			if thumbnailsPath is None:
				print "ignored : %s " % pfn
				continue
			assert pfn[0:len(path)] == path
			tfn = thumbnailsPath + pfn[len(path):]
			if not os.path.exists(tfn):
				print "%s -> %s" % (pfn,tfn)
				imgFilenames.append((pfn,tfn))
			
				
if __name__ == "__main__":

	print "Lino Publish"
	print copyleft(year='2002-2004')
	
	# collect names of files or directories containing uppercase
	# characters

	# os.path.walk(".",collect_upper,None)
	
	collect_upper()

	if len(upperDirnames)+len(upperFilenames) > 0 and confirm(
		"Okay to rename %d directories and %d files [Yn]?" %
				  (len(upperDirnames),len(upperFilenames))):
		
		for (o,n) in upperDirnames:
			os.rename(o,n)
		print "%d directories renamed" % len(upperDirnames)

		for (o,n) in upperFilenames:
			os.rename(o,n)
		print "%d files renamed" % len(upperFilenames)

	# collect names of image files

	collect_images()

	if len(imgFilenames) > 0 and confirm(\
		"Okay to create %d thumbnails [Yn]?" % len(imgFilenames)):
		# create thumbnails if they don't exist
		# TODO : check also timestamp, not only existence

		for (i,t) in imgFilenames:
			(head,tail) = os.path.split(t)
			if not os.path.exists(head):
				os.makedirs(head)
			im = Image.open(i)
			im.thumbnail(thumbnails_size) 
			im.save(t)


