#coding: latin1


from html import MemoParser

class TimMemoParser(MemoParser):
	def __init__(self,context):
		self._context = context
		cmds = {
			'url' : self.cmd_url,
			'ref' : self.cmd_ref,
			'xe' : self.cmd_ref,
			'logo' : self.cmd_logo,
			'btn' : self.cmd_btn,
			'img' : self.cmd_pic,
			'pic' : self.cmd_pic,
			}
		
		MemoParser.__init__(self,cmds)

	
	def cmd_btn(self,renderer,s):
		s = s.split(None,1)
		renderer.renderImage('buttons',*s)

	def cmd_logo(self,renderer,s):
		s = s.split(None,1)
		renderer.renderImage('logos',*s)

	def cmd_pic(self,renderer,s):
		a = s.split(None,1)
		renderer.renderPicture(*a)

	def cmd_ref(self,renderer,s):
		s = s.split(None,1)
		ref = s[0].split(':')
		if len(ref) != 2:
			return 
		try:
			if ref[0] == "MSX":
				ref[0] = "PAGES"
			elif ref[0] == "TPC":
				ref[0] = "TOPICS"
			elif ref[0] == "AUT":
				ref[0] = "AUTHORS"
			elif ref[0] == "NEW":
				ref[0] = "NEWS"
			elif ref[0] == "PUB":
				ref[0] = "PUBLICATIONS"
			ds = getattr(self._context,ref[0])
		except AttributeError,e:
			return 
			#return str(e)
		s[0] = renderer.uriToTable(ds._table)+"/"+ref[1]
		renderer.renderLink(*s)

	def cmd_url(self,renderer,s):
		s = s.split(None,1)
		renderer.renderLink(*s)
	## 	if len(s) == 2:
	## 		return renderLink(s[0],label=s[1])
	## 	else:
	## 		return renderLink(s[0])


	
