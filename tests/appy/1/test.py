# -*- coding: UTF-8 -*-
import os
import sys

from appy.pod.renderer import Renderer
from appy import version

print "appy.version.verbose", version.verbose
print "Python sys.version_info", sys.version
print "Python sys.platform", sys.platform

APPY_PARAMS = dict(ooPort=8100)
APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')

def run_test(number,HTML):
    tpl = 'test_template.odt'
    context = dict()
    context.update(HTML=HTML)
    target = 'test_result_%d.odt' % number
    if os.path.exists(target): 
        os.remove(target)
    renderer = Renderer(tpl, context, target,**APPY_PARAMS)
    renderer.run()  
    os.startfile(target)    


# 1 : this works fine with version 0.6.6
#~ run_test(1,'''
#~ <div class="document">
#~ <p>Hello, world?</p>
#~ </div>
#~ ''')

# 2 : this doesn't work with version 0.6.6, the list items are swallowed.
run_test(2,'''
<div class="document">
<p>Some <strong>bold</strong> and some <em>italic</em> text.</p>
<p>A new paragraph.</p>
<p>A list with three items:</p>
<ul> 
<li>the first item</li> 
<li>another item</li> 
<li>the last item</li> 
</ul> 
<p>A last paragraph.</p>
</div>
''')
    
#~ # 3 : the same as 3, but using `restify` to make the HTML
#~ from lino.utils.restify import restify
#~ run_test(3,restify(u'''
#~ Some **bold** and some *italic* text. 

#~ A new paragraph.

#~ A list with three items:

#~ - the first item
#~ - another item
#~ - the last item

#~ A last paragraph.
#~ '''))

