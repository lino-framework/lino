import re

def plain2xml(txt):
   txt = txt.replace("&","&amp;")
   txt = txt.replace("<","&lt;")
   return txt

memocommands = (
   ( re.compile('\[url\s+(\S+)\s*(.*?)\]',re.DOTALL),
     lambda m : '<b>'+m.group(2)+'</b> (<i>' + m.group(1)+ '</i>)'),
   )
# urlfind = 
# urlrepl = re.compile('<b>\2</b> (<u>\1</u>)')

# def urlrepl(m):
   


def memo2xml(txt):
   txt = plain2xml(txt)
   txt = txt.replace('[B]','<b>')
   txt = txt.replace('[b]','</b>')
   txt = txt.replace('[U]','<u>')
   txt = txt.replace('[u]','</u>')
   for find,repl in memocommands:
      txt = re.sub(find,repl,txt)
   return txt

def rst2xml(txt):
   raise "doesn't work"
   import docutils.parsers.rst
   import docutils.utils
   parser = docutils.parsers.rst.Parser()
   doc = docutils.utils.new_document("feed")
   parser.parse(txt, doc)
   raise "and now?"

_feeders={
   'xml' : lambda x : x,
   'plain' : plain2xml,
   'rst' : rst2xml,
   'memo' : memo2xml,
   }


def getFeeder(name):
   return _feeders[name]
