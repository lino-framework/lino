# $Id: lino.spec,v 1.6 2003/12/13 13:30:38 lsaffre Exp $
# (python-mode)
# Note: [C-x C-e : eval elisp expression before cursor]
import os

import shutil
import zipfile
from time import localtime, strftime

from lino.misc.console import confirm
from lino.misc.rdir import rdirlist

from lino import __version__
#from lino.releases import version, notes


global distDir # otherwise build() won't find it
distDir=r'c:\temp\lino'
zipDir=r'c:\temp\linozip'

global opj
opj = os.path.join

srcRoot = os.getcwd() # '.' # os.path.join('src','lino')
#wwwPath = opj(srcRoot,"docs","download")

srcZipName = r'%s\lino-src-%s.zip' % (zipDir,__version__)
if os.path.exists(srcZipName):
	if not confirm("Okay to remove %s?" % srcZipName):
		raise "Pilatus problem %s" % srcZipName
	os.remove(srcZipName)
	
binZipName = r'%s\timtools-%s.zip' % (zipDir,__version__)
if os.path.exists(binZipName):
	if not confirm("Okay to remove %s?" % binZipName):
		raise "Pilatus problem %s" % binZipName
	os.remove(binZipName)

if not os.path.exists(zipDir):
	os.makedirs(zipDir)
if not os.path.exists(distDir):
	os.makedirs(distDir)
l = os.listdir(distDir)
if len(l) > 0:
	if confirm("Delete %d files in %s ?" % (len(l),distDir)):
		shutil.rmtree(distDir)
		os.makedirs(distDir)


def build(name):
	a = Analysis([\
		  opj(HOMEPATH,'support','_mountzlib.py'),
		  opj(HOMEPATH,'support','useUnicode.py'),
		  name + '.py'],
		  pathex=[])
	pyz = PYZ(a.pure)
					 #a.scripts + [('v', '', 'OPTION')],
	exe = EXE(pyz,
				 a.scripts,
				 exclude_binaries=1,
				 name=opj(BUILDPATH,name+'.exe'),
				 debug=0,
				 strip=0,
				 upx=0,
				 console=1 )
	coll = COLLECT( exe,
						 a.binaries,
						 strip=0,
						 upx=0,
						 name=distDir)

#os.chdir(os.path.join('src','lino','timtools'))
os.chdir('scripts')

#targets = ['pds2pdf','prn2pdf','publish','sendmail']
targets = ['pds2pdf','prn2pdf','openmail']
for t in targets:
	build(t) 
	# confirm("Did the Build succeed?") or raise UserAbort

os.chdir(srcRoot)

def srcfilter(fn):
	if fn.endswith('~') : return False
	if fn.startswith('tmp') : return False
	root,ext = os.path.splitext(fn)
	if len(ext) :
		if ext.lower() in ('.pyc','.html','.zip','.pdf') :
			return False
	return True
##		return ext.lower() in ('.txt','.py','.bat', '.php',
##									  '.spec', '.pds', 'pin', '.sql',
##									  '.zip', '.jpg', '.gif')

zf = zipfile.ZipFile(srcZipName,'w',zipfile.ZIP_DEFLATED)

for root, dirs, files in os.walk(srcRoot):
	for fn in files:
		if srcfilter(fn):
			zf.write(opj(srcRoot,root,fn),opj(root,fn))
			
zf.close()	 

zf = zipfile.ZipFile(binZipName,'w',zipfile.ZIP_DEFLATED)
l = rdirlist(distDir)
for fn in l:
	zf.write(opj(distDir,fn),fn)
zf.write(os.path.join(srcRoot,'COPYING.txt'),'COPYING.txt')
zf.close()	 

## shutil.copy('COPYING.txt',distDir)

## os.chdir(distDir)
## cmd = r'zip %s *.*' % binZipName
## if not confirm(cmd):
##		raise UserAbort
## os.system(cmd)
## os.chdir(cwd)
