# -*- coding: utf-8 -*-

from HTMLParser import HTMLParser
from htmlentitydefs import name2codepoint

def attrs2xml(attrs):
    return ', '.join(['%s="%s"' % a for a in attrs])

class MyHTMLParser(HTMLParser):
    def __init__(self,*args,**kw):
        HTMLParser.__init__(self,*args,**kw)
        self.result = ''
        
    def handle_startendtag(self, tag, attrs):
        self.result += '<%s %s />' % (tag,attrs2xml(attrs))
        
    def handle_starttag(self, tag, attrs):
        self.result += '<%s %s>' % (tag,attrs2xml(attrs))

    def handle_endtag(self, tag):
        self.result += '</%s>' % tag
        
    def handle_data(self, data):
        self.result += data
        
    def handle_entityref(self,name):
        cp = name2codepoint.get(name,None)
        self.result += repr(cp)


def html2xhtml(html):
    p = MyHTMLParser()
    p.feed(html)
    p.close()
    return p.result




"""
Based on 
http://conmeomit.wordpress.com/2010/11/03/convert-html-to-xhtml-using-python/

"""


#~ OPENED=-10
#~ CLOSED=-20
#~ DEFAUTL_COUNT=100

#~ from sgmllib import SGMLParser

#~ class html_stripper(SGMLParser):
  #~ """remove all textes, i.e dataenu, except
  #~ links from a web page
  #~ Tags are kept"""
  #~ def reset(self):
    #~ SGMLParser.reset(self)
    #~ self.data=[]

  #~ def handle_data(self, text):
    #~ self.data.append([text])
    #~ pass

  #~ def unknown_starttag(self, tag, attrs):
    #~ parseAttrs=''.join ([' %s="%s"' % (k,v) for k,v in attrs ])

    #~ cell = ['%(tag)s' %locals(), DEFAUTL_COUNT, OPENED, '<%(tag)s%(parseAttrs)s>' %locals() ]
    #~ self.data.append(cell)

  #~ def unknown_endtag(self, tag):

    #~ cell = ['%(tag)s' %locals(), DEFAUTL_COUNT,CLOSED, '</%(tag)s>' %locals()]
    #~ self.data.append(cell)








#~ def reconstruct(data):
    #~ '''return the code html of data'''
    #~ html_txt = ""
    #~ for cell in data:
      #~ if len(cell) == 1:
        #~ #text
        #~ html_txt = html_txt +  cell[0]
      #~ elif len(cell)>=4:
        #~ #tag
        #~ html_txt = html_txt + cell[3]
    #~ return html_txt

#~ def update_count(data):
    #~ '''update the count attribute in data'''
    #~ return
    #~ print data
    #~ html_tag_pos = 0 #position of html tag
    #~ while len(data[html_tag_pos]) < 2 or data[html_tag_pos][0]!= 'html':
      #~ html_tag_pos += 1
      #~ print html_tag_pos

    #~ data[html_tag_pos][1] = 1
    #~ tmp = 1
    #~ for pos in range(html_tag_pos + 1,len(data)):
      #~ if len(data[pos]) > 2 :
        #~ if data[pos][2] == OPENED:
          #~ data[pos][1] = tmp + 1
          #~ tmp = data[pos][1]
        #~ else:
          #~ data[pos][1] = tmp -1
          #~ tmp = data[pos][1]

#~ def add_missing_tag(data):
  #~ '''add missing tag'''

  #~ #all_tag = [cell[0] for cell in data ]
  #~ #print all_tag

  #~ #missing_tag = [] #list of all tag that misses closed tag
  #~ #for tag in all_tag:
    #~ #open_tag  = [x for x in data if x[0] == tag and x[2] == OPENED]
    #~ #close_tag = [x for x in data if x[0] == tag and x[2] == CLOSED]
    #~ #if len(open_tag) == len (close_tag):
      #~ #missing_tag.append(tag)
  #~ #print missing_tag

  #~ #detecting position where missing tag resides
  #~ missing_pos = []
  #~ for pos in range(0,len(data)):
    #~ #print 'attacking:', pos, data[pos] #debug
    #~ cell = data[pos]
    #~ # missing tag are always open
    #~ if len(cell) > 2 and  cell[2]==OPENED:
      #~ # the open tag corresponding to cell[0]
      #~ corresponding_open_tag = [x for x in data[pos+1:] if x[0] == cell[0] and x[2] == OPENED]
      #~ corresponding_close_tag = [x for x in data[pos+1:] if x[0] == cell[0] and x[2] == CLOSED]

      #~ if len(corresponding_open_tag) > len(corresponding_close_tag):
        #~ #tag cell[0] surely misses something -> save its pos in missing_pos
        #~ missing_pos.append(pos)
      #~ elif 	len(corresponding_open_tag) == len(corresponding_close_tag):
        #~ if len(corresponding_open_tag) == 0:
          #~ missing_pos.append(pos)
        #~ else:
          #~ #print 'the most complicate one'
          #~ #the most complicate one
          #~ next_pos = pos + 1 # position of the next cell whose tag is the same as cell
          #~ while data[next_pos][0] != cell[0] :
            #~ #print 'next_pos=', next_pos #debug
            #~ next_pos += 1
          #~ if data[next_pos][2] == OPENED:
            #~ missing_pos.append(pos)
          #~ else:
            #~ pass

    #~ else:
      #~ pass

  #~ #print missing_pos #debug

  #~ #adding missing tag to all tag at missing_pos
  #~ for i in range(0,len(missing_pos)):
    #~ pos = missing_pos[i]
    #~ cell = data[pos]
    #~ new_cell = [cell[0],DEFAUTL_COUNT, CLOSED, '</' + cell[0]+ '>' ] #the missing tag is always an open one
    #~ #print pos, data[pos], data[:pos+1], data[:pos+1]+[cell]+data[pos+1:] # debugging
    #~ data = data[:pos+1]+ [new_cell] + data[pos+1:]

    #~ #add 1 to all position in missing_pos
    #~ for j in range(i+1,len(missing_pos)):
      #~ missing_pos[j] += 1

  #~ return data

#~ def display(data):
    #~ '''print data in a easy reading form'''
    #~ f = lambda x: (x==-10) and 'OPENED' or 'CLOSED'
    #~ g = lambda x: (x<0) and f(x) or repr(x)
    #~ res = []
    #~ res.append("--------------------------------------------")
    #~ print (">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
    #~ print "length=",len(data)
    #~ size = 10
    #~ s = 'position'.ljust(size)+ 'tag'.ljust(size) + 'count'.ljust(size) + 'type'.ljust(size) + 'href'.ljust(size)
    #~ res.append(s)
    #~ res.append("--------------------------------------------")

    #~ for pos  in range(0,len(data)):
      #~ cell = data[pos]
      #~ s=repr(pos).ljust(size)
      #~ for x in cell:
        #~ s += g(x).ljust(10)
      #~ res.append(s)
    #~ print "\n".join(res)
  
  
#~ def html2xhtml(html):
    #~ p = html_stripper()
    #~ p.feed(html)
    #~ p.close()
    #~ data = add_missing_tag(p.data)
    #~ update_count(data)
    #~ return reconstruct(data)
  

#~ class html2xhtml():
  
  #~ def __init__(self,url):
    #~ self.url = url
    #~ self.page=""
    
  #~ def feed(self,instream):
    #~ strip = html_stripper()
    #~ strip.feed(instream)
    #~ strip.close()
    #~ data = strip.data

    #~ #add missing tag test
    #~ data = add_missing_tag(data)
    #~ update_count(data)

    #~ self.page = reconstruct(data)

#~ if __name__ == "__main__"	:
  
  #~ import sys
  
  #~ if len(sys.argv) != 3:
    #~ print 'usage: html2xhtml url(local file or link) output_file'
    #~ print 'note that, if url is not a file, it must have prefix like http:// or ftp://'

  #~ else:
    #~ url = sys.argv[1]
    #~ output_file = file(sys.argv[2], 'w')
    #~ print 'url=', url
    #~ print 'output_file=', sys.argv[2]
    #~ convert = html2xhtml(url)

    #~ import os.path
    #~ if os.path.isfile(url):
      #~ convert.feed(open(url).read())
      #~ output_file.write(convert.page)
    #~ else:
      #~ import urllib
      #~ fop = urllib.urlopen(url)
      #~ convert.feed (fop.read())
      #~ fop.close()
      #~ output_file.write(convert.page)
      
      
if __name__ == "__main__"	:
    html = '''
    <p>Hello,&nbsp;world!<br>Again I say: Hello,&nbsp;world!</p>
    <img src="foo.org">
    '''
    print html
    print html2xhtml(html)
    
    #~ print html2xhtml('''
    #~ <p><span style="background-color: rgb(255, 255, 255); " id="ext-gen416">
    #~ Also ich probier mal.<br/>Schreibe ein bisschen Text.<br/><br/></span>
    #~ <h1 id="ext-gen418"><span style="background-color: rgb(255, 255, 255); ">
    #~ <span style="font-size: 32px; font-weight: bold; " id="ext-gen408">Aufzählungen:</span></span></h1>
    #~ <ol><li>Eins</li><li>Zwei</li><li>Drei</li><li>Vier</li><li>Fünf</li></ol><span style="background-color: rgb(255, 255, 255); "><br/><div id="ext-gen420"><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">
    #~ Aber für :field:`notes</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 
    #~ 2px; -webkit-border-vertical-spacing: 2px;">.Note.body` 
    #~ gilt das nicht.&nbsp;</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; ">Dafür ist er ideal. Auch der Ausdruck funktioniert einfach,&nbsp;</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; ">indem ich in&nbsp;</span><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; "><a href="https://github.com/VinylFox/ExtJS.ux.HtmlEditor.Plugins" target="_self">appy.pod</a></span></div><div id="ext-gen420"><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; ">die folgende Formel verwende::</span></div><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; "><br/></span></div></span><blockquote class="webkit-indent-blockquote" style="margin: 0 0 0 40px; border: none; padding: 0px;"><span style="background-color: rgb(255, 255, 255); "><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">&nbsp; do text</span></div></span><span style="background-color: rgb(255, 255, 255); "><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">&nbsp; from xhtml(self.body)</span></div></span></blockquote><span style="background-color: rgb(255, 255, 255); "><div><span style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px;">&nbsp;&nbsp;</span></div><div style="border-collapse: collapse; -webkit-border-horizontal-spacing: 2px; -webkit-border-vertical-spacing: 2px; "><br/></div></span></p>
    #~ ''')
    