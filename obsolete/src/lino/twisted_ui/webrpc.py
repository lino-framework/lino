#coding: latin1
#---------------------------------------------------------------------
# webrpc.py
# Copyright: (c) 2004 Luc Saffre
# License:	 GPL
#----------------------------------------------------------------------

"""
Idee: 
In der Webanwendung deklariere ich alle "erlaubten" Befehle, sodass die Twisted-Resource diese Methoden veröffentlicht. 
Wenn ein Client z.B. 

	http://www.example.com/test/show/PARTNERS?ob=tel%20email
	
aufruft, dann findet Twisted die WebrpcResource "test" und ruft deren render auf (sucht nicht selber nach einem child namens show, weil isLeaf=True ist). Die Resource wurde wie folgt deklariert:

	rsc = WebrpcResource()
	m = rsc.addMethod('show','showReport')
	m.addAgument( lambda s: return db.getDatasource(s), lambda ds: return ds.getTableName() )
	m.addKeyword('ob','orderBy', lambda t : return " ".join(t), lambda t : return " ".join(t))
	m.addKeyword('st', 'showTitle', lambda t : return (t[0].lower() in ('1','yes','t')))

automatisch die entsprechende Methode aufruft, wobei die positional arguments und keywords 
Also ein RPC-Server, der über URLs arbeitet.
"""



z.B. 

TwistedSession.showReport(self,ds,columnNames=None,showTitle=True,**kw):




class WebrpcMethod:
def __init__(self,meth):
	self.method = meth
	self.argspecs = []
	self.kwspecs = []
def addArgument(self,url2value,value2url):
	self.argspecs.append( (url2value,value2url) )
def addKeyword(self,short,long,url2value,value2url):
	self.argspecs.append( (url2value,value2url) )

class WebrpcResource(twisted.Resource):
def __init__(self,target)
	self.target = target
	self.methods = {}
def addMethod(self,meth,name=None,label=None,doc=None)
	m = WebRpcMethod(meth,label,doc)
	if name is None:
		name = meth.__name__
   self.methods[name] = m
	return m
def exec(self,url):
	





