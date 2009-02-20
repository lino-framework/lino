import os

from docutils import core 
from docutils.parsers.rst.directives.admonitions import BaseAdmonition
from docutils.parsers.rst import directives
from docutils import nodes 
from docutils.parsers import rst

class Question(BaseAdmonition):
    has_content = True
    node_class = nodes.admonition
  
    """Subclasses must set this to the appropriate admonition node class."""


directives.register_directive("question", Question)
directives.register_directive("answer", Question)
directives.register_directive("vocabulary", Question)
directives.register_directive("instruction", Question)
directives.register_directive("remark", Question)

import codecs
f=codecs.open(os.path.join("data","pkk","pkk.rst"),"r","utf8")

doctree = core.publish_doctree(f.read())

for p in doctree:
    print p.__class__
    for sp in p:
        print "  ", sp.__class__
        
course=Course()
entry=Entry(course=self)
for elem in doctree:
    if isinstance(elem,nodes.Titular):
    if isinstance(elem,nodes.Structural):
      

#~ for k, v in doctree.items():
  #~ print "-", k, ":", type(v)

#~ print type(doctree["whole"])

#for part in doctree["whole"][:10]:
#  print repr(part)

