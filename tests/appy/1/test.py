# -*- coding: UTF-8 -*-
import os
import sys

from appy.pod.renderer import Renderer
from appy import version

print "appy.version.verbose", version.verbose
print "Python sys.version_info", sys.version
print "Python sys.platform", sys.platform

APPY_PARAMS = dict()

#~ APPY_PARAMS.update(ooPort=8100)
#~ APPY_PARAMS.update(pythonWithUnoPath=r'C:\PROGRA~1\LIBREO~1\program\python.exe')

def run_test(number,title,HTML):
    tpl = 'test_template.odt'
    context = dict(locals())
    context.update(
        appy_version=version.verbose,
        python_version=sys.version,
        platform=sys.platform,
    )
    target = 'test_result_%d.odt' % number
    if os.path.exists(target): 
        os.remove(target)
    renderer = Renderer(tpl, context, target,**APPY_PARAMS)
    renderer.run()  
    print "Generated file", target
    #~ os.startfile(target)    


# 1 : 
#~ run_test(1,"Simple test. Works fine with version 0.6.6", '''
#~ <div class="document">
#~ <p>Hello, world?</p>
#~ </div>
#~ ''')

# 2 : 
run_test(2,"List items are not rendered (Appy 0.6.6)",'''
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
    
#~ # 3 : the same as 2, but using `restify` to make the HTML
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

from lino.utils.restify import restify
run_test(4,"List items are not rendered (Appy 0.6.6), but using `restify` to make the HTML",restify(u'''
Längere Texte mit mehreren Absätzen im Inhalt einer Notiz (Note.body) 
wurden in der Grid zu einem einzigen Absatz zusammengeschnürt. 

- Virtuelles Feld `body_html` benutzt `lino.utils.restify`
- `body` ist jetzt in der Grid unsichtbar

Das Resultat ist jetzt einigermaßen akzeptabel (`Links <http://lino.saffre-rumma.net>`_ sind anklickbar, 
Absatzwechsel werden als Zeilenwechsel angezeigt), aber noch nicht 
optimal (**fett**, *kursiv*, Aufzählungen werden verschluckt).
'''))
