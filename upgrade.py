import os.path as op
import os
from lino.misc.console import confirm

def cvs_rename(dirname,oldname,newname):
	raise NotImplementedError
	src = op.join(dirname,oldname)
	dest = op.join(dirname,newname)
	os.rename(src,dest)
	os.system("cvs remove")

class Upgrader:
	def __init__(self,f,v1,v2):
		self.f = f
		self.v1 = v1
		self.v2 = v2
	def run(self):
		return self.f()
		
upgraders = []

def declare_upgrader(f,v1,v2):
	upgraders.append(Upgrader(f,v1,v2))

	
def upgrade_0_5_4(dataRoot):
	"WebMan : init.py now named init.wmi"
	todo_rename = []
	for (root,dirs,files) in os.walk(dataRoot):
		for fn in files:
			if fn == "init.py":
				todo_rename.append((op.join(root,fn),
										  op.join(root,"init.wmi")))
	for (src,dest) in todo_rename:
		print "rename %s to %s" % (src,dest)
	if not confirm("okay"):
		return False
	for (src,dest) in todo_rename:
		os.rename(src,dest)
	return True

declare_upgrader(upgrade_0_5_4,None,"0.5.4")


if __name__ == "__main__":

 	dataRoots = ['.']
## 	#oldVersion = op.join(myDataRoot,'lino.mrk'))
## 	oldVersion = ""
## 	newVersion = "0.5.4"
	
## 	v = oldVersion
	
## 	for u in upgraders:
## 		if u.v1 is None or u.v1 == v1:
## 			if u.f(
## 			if u.v2 is None or u.v2 == v2:

	for dr in dataRoots:
		upgrade_0_5_4(dr)


