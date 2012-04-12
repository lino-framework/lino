# -*- coding: UTF-8 -*-
## Copyright 2011-2012 Luc Saffre
## This file is part of the Lino project.
## Lino is free software; you can redistribute it and/or modify 
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
## Lino is distributed in the hope that it will be useful, 
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the 
## GNU General Public License for more details.
## You should have received a copy of the GNU General Public License
## along with Lino; if not, see <http://www.gnu.org/licenses/>.

import logging
#~ logging.basicConfig(filename='example.log',level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


import os
import codecs
import locale
import re


from lino.utils import AttrDict
from lino.utils import iif, curry
from lino.utils import memo
from lino.utils.html2xhtml import html2xhtml

from lino.utils.restify import restify
from lino.utils.rstgen import SimpleTable, write_header, html2rst
from lino.utils import htmlgen
from lino.utils import uca_collator

USE_XHTML2ODT = False

if USE_XHTML2ODT:

    from Cheetah.Template import Template as CheetahTemplate
    import xhtml2odt
    class MyODTFile(xhtml2odt.ODTFile):
      
        def render(self,context):
            self.open()
            tpl = CheetahTemplate(self.xml['content'],namespaces=[context])
            nc = unicode(tpl) #.encode('utf-8')
            if nc.startswith('<?xml version'):
                #~ nc = nc.replace('<?xml version="1.0" encoding="UTF-8"?>','')
                nc = nc.split('\n',1)[1]
            self.xml['content'] = nc
            #~ odt = self.xhtml_to_odt(xhtml)
            #~ self.insert_content(odt)
            if True:
                f = open("content.xml","wt")
                f.write(self.xml['content'].encode('utf-8'))
                f.close()
            self.add_styles()
            self.save(self.options.output)

pronunciationRE = re.compile("^(.*)\s*(\[.*\])\s*",re.DOTALL)


def makedirs_if_missing(dirname):
    if dirname and not os.path.isdir(dirname):
        os.makedirs(dirname)


class LanguageMeta(type):
  
    def __new__(meta, classname, bases, classDict):
        # Each subclass gets her own list of word types:
        classDict['words'] = []
        classDict['wordTypes'] = []
        cls = type.__new__(meta, classname, bases, classDict)
        return cls


class Language(object):
    __metaclass__ = LanguageMeta
    
    @classmethod
    def add_wordtype(cls,wt):
        cls.wordTypes.append(wt)
        
    @classmethod
    def register_word(cls,w):
        for ew in cls.words:
            if ew == w:
                return ew
        cls.words.append(w)
        return w
        

class WordType(object):
    text = None
    @classmethod
    def is_of_this_type(cls,w):
        return w.type == cls



class Word(object):
    type = None
    text = None
    pronounciation = ''
    gender = None
    form = None
  
    def __init__(self,text,
        type=None,
        pronounciation=None,
        gender=None,
        form=None):
        if not text:
            raise Exception("Cannot create empty word!")
        self.text = text
        if type: self.type = type
        if form is not None: self.form = form
        if pronounciation: 
            assert pronounciation.startswith('[')
            assert pronounciation.endswith(']')
            self.pronounciation = pronounciation[1:-1]
        if gender:
            assert gender in ('m','f','mf','pl')
            self.gender = gender
        self.translations = []
        self.units = []
        
    def get_pron_html(self,article=False):
        if not self.pronounciation:
            return ''
        #~ if article and Nom.is_of_this_type(self):
            
        return "[%s]" % self.pronounciation
        
    def add_to_unit(self,unit):
        self.units.append(unit)
        #~ unit.add_word(self)
        
    def __repr__(self):
        return "%r(%r)" % (self.text,self.type.__name__)
        
    def __eq__(self,other):
        if self.__class__ != other.__class__: return False
        if self.text != other.text: return False
        if self.pronounciation != other.pronounciation: return False
        if self.gender != other.gender: return False
        if self.type != other.type: return False
        return True
        
    def add_translations(self,translations):
        for t in translations:
            if not t in self.translations:
                self.translations.append(t)
                
    def opposite_gender(self):
        if self.gender == 'f' : return 'm'
        if self.gender == 'm' : return 'f'
        return None
        
    def get_partner(self,gender):
        if self.gender == 'mf' or self.gender == gender:
            return self
        if not self.partner:
            raise Exception("%r has no partner " % self)
        return self.partner
        




class Column:
    label = ''
    def __init__(self,label):
        self.label = label
        
    @classmethod
    def render(cls,w,book):
        s = html2rst(cls.word2html(w,book))
        if s.startswith('('):
            s = '\\' + s
        return s
        
    @classmethod
    def word2html(cls,w,book):
        raise NotImplementedError()
        

class FR(Column):
    
    label = 'prantsuse k.'
    
    @classmethod
    def word2html(cls,w,book):
        return book.from_language.present_word2html(w,book)
        

class PRON(Column):
    label = u'hääldamine'
    @classmethod
    def word2html(cls,w,book):
        return w.get_pron_html()

class ET(Column):
    label = u'eesti k.'
    @classmethod
    def word2html(cls,w,book):
        if len(w.translations) == 1:
            return w.translations[0]
        return "; ".join(["(%d) %s" % (n+1,w) for n,w in enumerate(w.translations)])
    
        
class M(Column):
    label = u'meessoost'
    gender = 'm'
    @classmethod
    def word2html(cls,w,book):
        #~ return html2rst(w.html_fr_lesson()) + ' ' + w.pronounciation
        w = w.get_partner(cls.gender)
        return '<b>%s</b>' % w.text + ' ' + w.get_pron_html()
        
class F(M):
    label = u'naissoost'
    gender = 'f'
        

class GEON(FR):
    label = u'Maa'

class GEOM(Column):
    gender = 'm'
    label = u'omadussõna (m)'
    @classmethod
    def word2html(cls,w,book):
        if not w.adjectif:
            return ''
        w = w.adjectif
        w = w.get_partner(cls.gender)
        return '<b>%s</b>' % w.text + ' ' + w.get_pron_html()
        #~ return html2rst('<b>%s</b>' % w.text) + ' ' + w.get_pron_html()
        
class GEOF(GEOM):
    label = u'omadussõna (n)'
    gender = 'f'



#~ def mycmp(a,b):
    #~ return locale.strcoll(a,b)
        
def sort_by_fr(a,b):
    return locale.strcoll(a.text.lower(),b.text.lower())
    #~ return locale.strcoll(S(a.fr),S(b.fr))
    

class Section:
    def __init__(self,book,parent,
            title=None,intro=None,
            number=None,ref=None,
            from_language=None,
            to_language=None):
        if from_language is None:
            from_language = parent.from_language
        if to_language is None:
            to_language = parent.to_language
        #~ if number is None:
            #~ raise Exception("Section %r has no number" % title)
        self.to_language = to_language
        self.from_language = from_language
        self.parent = parent
        if number is not None:
            if not isinstance(number,int):
                raise Exception("Section %r got invalid number %r" % (title,number))
        elif parent is not None:
            number = len(parent.children) + 1
        self.number = number
        self.book = book
        self.ref = ref
        self.title = title
        self.intro = intro
        self.body = []
        self.words = []
        self.children = []
        self.current_lesson = None
        if self.ref:
            if self.ref in self.book.ref2sect:
                raise Exception("Duplicate reference %r" % self.ref)
            self.book.ref2sect[self.ref] = self
        
    def add_section(self,*args,**kw):
        sect = Section(self.book,self,*args,**kw)
        self.children.append(sect)
        return sect
        
    def add_index(self,*args,**kw):
        sect = Index(self.book,self,*args,**kw)
        self.children.append(sect)
        return sect
        
    def add_dictionary(self,*args,**kw):
        sect = Dictionary(self.book,self,*args,**kw)
        self.children.append(sect)
        return sect
        
    def add_lesson(self,*args,**kw):
        self.current_lesson = Unit(self.book,self,*args,**kw)
        self.children.append(self.current_lesson)

    def add_after(self,chunk):
        #~ self.current_lesson.body.append(chunk)
        self.current_lesson.after.append(chunk)
        
    def parse_words(self,cl,lines):
        self.current_lesson.parse_words(cl,lines)
        
    def name_parts(self):
        if self.parent is None:
            return ['index' ]
        elif self.children:
            return [ self.get_ref(), 'index' ]
        else:
            return [ self.get_ref() ]
      
    def get_ref(self):
        if self.ref:
            return self.ref
        if self.number is not None:
            #~ return str(self.number)
            return '%02d' % self.number
        
    def rst_ref_to(self,text=None):
        parts = self.name_parts()
        #~ ref = self.get_ref()
        p = self.parent
        while p is not None:
            pref = p.get_ref()
            #~ if p.number is not None:
            if pref is not None:
                #~ parts = ['%02d' % p.number] + parts
                parts = [pref] + parts
            p = p.parent
        if not text:
            text = self.get_ref_text()
        if text:
            return ':doc:`%s </%s>`' % (text,'/'.join(parts))
        return ':doc:`/%s`' % '/'.join(parts)
        #~ return ':doc:`%s </%s>`' % (self.title,'/'.join(parts))
        
    def get_full_number(self):
        number = str(self.number)
        p = self.parent
        while p is not None:
            if p.number is not None:
                number = str(p.number) + "." + number
            p = p.parent
        return number
        
    def get_ref_text(self):
        return self.title
        
    def html_lines(self,level=1):
        if self.number is None:
            title = self.title
        else:
            title = "%s %s" % (self.get_full_number(),self.title)
        if True:
            if self.parent is not None:
                title = htmlgen.restify(self.memo2rst(title)).strip()
                if title.startswith('<p>') and title.endswith('</p>'):
                    title = title[3:-4]
                    #~ logger.info("20120311 title is %r", title)
                else:
                    raise Exception("20120311 title is %r" % title)
                    
                yield htmlgen.H(level,title)
        else:
            tag = "H%d" % level
            title = title.replace("<p>","<"+tag+">")
            title = title.replace("</p>","</"+tag+">")
            yield title
            #~ yield "<H%d>%s</H%d>" % (level,,level)
        
        if self.intro:
            yield htmlgen.restify(self.memo2rst(self.intro))
            
        if self.children:
            for s in self.children:
                for ln in s.html_lines(level+1):
                    yield ln
                    
        for chunk in self.body:
            yield htmlgen.restify(self.memo2rst(chunk))
        
        
    def write_rst_files(self,root):
        fn = os.path.join(root,*self.name_parts()) + ".rst"
        logger.info("Generate %s",fn)
        newroot = os.path.dirname(fn)
        makedirs_if_missing(newroot)
        fd = codecs.open(fn,'w','utf-8')
        
        if self.number is None:
            title = self.title
        else:
            title = "%d. %s" % (self.number,self.title)
            
        #~ if self.number is None:
            #~ write_header(fd,1,"%s" % self.title)
        #~ else:
            #~ write_header(fd,1,"%d. %s" % (self.number,self.title))
        write_header(fd,1,self.memo2rst(title))
        self.write_body(fd)
        fd.close()
        for s in self.children:
            s.write_rst_files(newroot)

    def write_body(self,fd):
        if self.intro:
            fd.write(self.memo2rst(self.intro) + '\n\n')
            
        for chunk in self.body:
            fd.write(self.memo2rst(chunk) + '\n\n')
        

        if self.children:
            fd.write("""\
.. toctree::
   :maxdepth: 2
   
""")
            for s in self.children:
                fd.write("   "  + ("/".join(s.name_parts())) + "\n")
            fd.write('\n\n')


    def memo2rst(self,s):
        return self.book.memo2rst(s)



class Unit(Section):
    columns = [FR,PRON,ET]
    def __init__(self,book,parent,title=None,intro=None,columns=None,show_headers=None,**kw):
        if columns is not None:
            self.columns = columns
            if show_headers is None:
                show_headers = True
        elif show_headers is None:
            show_headers = False
        self.show_headers = show_headers
        #~ self.parent = parent
        Section.__init__(self,book,parent,title=title,intro=intro,**kw)
        if not self.title:
            self.title = u"Leçon %d" % self.number
        self.after = []
        #~ if after:
            #~ self.add_after(after)
        self.words = []
        
    #~ def add_word(self,w):
        #~ self.words.append(w)
        
    def tablerow(self,w):
        return [col.render(w,self) for col in self.columns]
          
    def parse_words(self,cl,lines):
        #~ lesson = self.current_lesson
        for ln in lines.splitlines():
            ln = ln.strip()
            if ln and not ln.startswith('#'):
                a = ln.split(':')
                if len(a) != 2:
                    raise Exception("%r.split(':') is not 2" % ln)
                fr_list = a[0].split('|')
                et_list = a[1].split('|')
                
                translations = []
                for et in et_list:
                    et = et.strip()
                    if et == '-':
                        pass
                    elif et.startswith('#'):
                        pass
                    else:
                        w = self.to_language.parse_word(et)
                        translations.append(et)
                main = None
                for fr in fr_list:
                    w = self.from_language.parse_word(fr,cl,parent=main) 
                    w.add_to_unit(self)
                    #~ w.add_lesson(self.current_lesson)
                    w.add_translations(translations)
                    if main:
                        main.marry(w)
                    else:
                        main = w
                self.words.append(main)

          
        
    def html_lines(self,level=1):
        for ln in Section.html_lines(self,level):
            yield ln
        words = [w for w in self.words if w.parent is None]
        if words:
            t = htmlgen.TABLE([col.label for col in self.columns],
                    show_headers=self.show_headers)
            def row(w):
                return [col.word2html(w,self) for col in self.columns]
            rows = [row(w) for w in words]
            for ln in t.html_lines(rows):
                yield ln
        for chunk in self.after:
            yield restify(self.memo2rst(chunk))
            
    def write_body(self,fd):
      
        Section.write_body(self,fd)
        
        words = [w for w in self.words if w.parent is None]
        if words:
            t = SimpleTable([col.label for col in self.columns],
                    show_headers=self.show_headers)
            t.write(fd,[self.tablerow(w) for w in words])
          
        for chunk in self.after:
            fd.write('\n\n' + chunk + '\n\n')
            


def uca_sort(l):
    c = uca_collator()
    def k(w): return c.sort_key(w.text)
    l.sort(key=k)

  
  
            
            
            
class Dictionary(Section):
    columns = [FR,PRON,ET]
    show_headers = True
    def html_lines(self,level=1):
        for ln in Section.html_lines(self,level):
            yield ln
        words = [w for w in self.from_language.words if w.parent is None]
        if words:
            uca_sort(words)
            t = htmlgen.TABLE([col.label for col in self.columns],
                    show_headers=self.show_headers)
            def row(w):
                return [col.word2html(w,self) for col in self.columns]
            rows = [row(w) for w in words]
            for ln in t.html_lines(rows):
                yield ln
            
  
class Index(Section):
    def html_lines(self,level=1):
        for ln in Section.html_lines(self,level):
            yield ln
        #~ self.from_language.words.sort(sort_by_fr)
        uca_sort(self.from_language.words)
        #~ self.from_language.words = uca_sorted(self.from_language.words)
        def fmt(w):
            return self.from_language.word2html(w) \
            + " " + ET.word2html(w,self) \
            + " " \
            + ", ".join([u.get_full_number() for u in w.units])
        for w in self.from_language.words:
            yield "<br>" + fmt(w)
            
    def write_body(self,fd):
        Section.write_body(self,fd)
        self.from_language.words.sort(sort_by_fr)
        uca_sort(self.from_language.words)
        #~ self.from_language.words = uca_sorted(self.from_language.words)
        def fmt(w):
            return self.from_language.word2html(w) \
            + " " + ET.word2html(w,self) \
            + " " \
            + ", ".join([u.rst_ref_to() for u in w.units])
        for w in self.from_language.words:
            fd.write("| %s\n" % html2rst(fmt(w)))
                
class MemoParser(memo.Parser):
    def __init__(self,book,*args,**kw):
        self.book = book
        memo.Parser.__init__(self,*args,**kw)
        self.register_command('ref',self.cmd_ref)
        self.register_command('item',curry(self.cmd_item,'- '))
        self.register_command('oitem',curry(self.cmd_item,'#. '))
        self.register_command('ruleslist',self.cmd_ruleslist)
        
    def cmd_ref(self,s):
        sect = self.book.ref2sect[s]
        return sect.rst_ref_to()

    def cmd_item(self,prefix,ref,rulesmode=False):
        indent = " " * len(prefix)
        sect = self.book.ref2sect[ref]
        r = prefix 
        if not rulesmode:
            r += sect.rst_ref_to() 
            if sect.intro:
                r += " -- "
        if sect.intro:
            intro = self.book.memo2rst(sect.intro.strip())
            if "\n\n" in intro:
                r += "\n"
                for ln in intro.splitlines():
                    r += indent + ln + "\n"
                r += "\n"
            else:
                intro = intro.replace('\n','\n'+indent)
                r += intro
        if rulesmode:
            r += "\n" + indent + "-- " + sect.rst_ref_to(text=sect.get_full_number())
        r += "\n"
        return r
        
    def cmd_ruleslist(self,s):
        r = ''
        for ref in s.split():
            r += self.cmd_item('#. ',ref,rulesmode=True)
        return r
            
  
class Book:
    def __init__(self,from_language,to_language,
          title=None,input_template=None,
          memo_parser=None):
        self.input_template = input_template
        self.ref2sect = dict()
        self.memo_parser = memo_parser or MemoParser(self)
        self.main = Section(self,None,title,
            from_language=from_language,to_language=to_language)

    def memo2rst(self,s):
        return self.memo_parser.parse(s)

    def add_section(self,*args,**kw): return self.main.add_section(*args,**kw)
    def add_index(self,*args,**kw): return self.main.add_index(*args,**kw)
    def add_dictionary(self,*args,**kw): return self.main.add_dictionary(*args,**kw)
      
        
    def old_as_odt(self):
        from xhtml2odt import ODTFile
        from lino.utils import AttrDict
        from lino.utils.html2xhtml import html2xhtml
        options = AttrDict(
          url = "",
          with_network = False,
          verbose = True,
          template = self.input_template,
          top_header_level = 1,
          img_width = "8cm",
          img_height = "6cm",
          )
        
        #~ version=False # help="Show the version and exit")
        #~ input=input", metavar="FILE",
                          #~ help="Read the html from this file")
        #~ parser.add_option("-o", "--output", dest="output", metavar="FILE",
                          #~ help="Location of the output ODT file")
        #~ parser.add_option("-t", "--template", dest="template", metavar="FILE",
                          #~ help="Location of the template ODT file")
        #~ parser.add_option("-u", "--url", dest="url",
                          #~ help="Use this URL for relative links")
        #~ parser.add_option("-v", "--verbose", dest="verbose",
                          #~ action="store_true", default=False,
                          #~ help="Show what's going on")
        #~ parser.add_option("--html-id", dest="htmlid", metavar="ID",
                          #~ help="Only export from the element with this ID")
        #~ parser.add_option("--replace", dest="replace_keyword",
                          #~ default="ODT-INSERT", metavar="KEYWORD",
                          #~ help="Keyword to replace in the ODT template "
                          #~ "(default is %default)")
        #~ parser.add_option("--cut-start", dest="cut_start",
                          #~ default="ODT-CUT-START", metavar="KEYWORD",
                          #~ help="Keyword to start cutting text from the ODT "
                          #~ "template (default is %default)")
        #~ parser.add_option("--cut-stop", dest="cut_stop",
                          #~ default="ODT-CUT-STOP", metavar="KEYWORD",
                          #~ help="Keyword to stop cutting text from the ODT "
                          #~ "template (default is %default)")
        #~ parser.add_option("--top-header-level", dest="top_header_level",
                          #~ type="int", default="1", metavar="LEVEL",
                          #~ help="Level of highest header in the HTML "
                          #~ "(default is %default)")
        #~ parser.add_option("--img-default-width", dest="img_width",
                          #~ metavar="WIDTH", default="8cm",
                          #~ help="Default image width (default is %default)")
        #~ parser.add_option("--img-default-height", dest="img_height",
                          #~ metavar="HEIGHT", default="6cm",
                          #~ help="Default image height (default is %default)")
        #~ parser.add_option("--dpi", dest="img_dpi", type="int",
                          #~ default=96, metavar="DPI", help="Screen resolution "
                          #~ "in Dots Per Inch (default is %default)")
        #~ parser.add_option("--no-network", dest="with_network",
                          #~ action="store_false", default=True,
                          #~ help="Do not download remote images")
        #~ options, args = parser.parse_args()
        odtfile = ODTFile(options)
        odtfile.open()
        
        xhtml = ''.join([ln for ln in self.main.html_lines()])
        xhtml = html2xhtml(xhtml)
        #~ xhtml = "<DIV>%s</DIV>" % xhtml
        xhtml = """\
<html xmlns="http://www.w3.org/1999/xhtml"><body>%s</body></html>""" % xhtml
        #~ xhtml = "<p>%s</p>" % xhtml
        if True:
            f = open("before.xml","wt")
            f.write(xhtml.encode('utf-8'))
            f.close()
        
        #~ logger.info("Gonna do it with %r",xhtml)
        xhtml = odtfile.xhtml_to_odt(xhtml)
        if True:
            f = open("after.xml","wt")
            f.write(xhtml)
            #~ f.write(xhtml.encode('utf-8'))
            f.close()
        return xhtml
        
    def html(self):
        #~ s = htmlgen.DIV(self.main.html_lines)
        s = ''.join([ln for ln in self.main.html_lines()])
        s = "<div>%s</div>" % s
        #~ logger.info(s)
        return s
        
        
    def write_rst_files(self,root='.'):
        
        self.main.write_rst_files(root)
        
        if False: # must convert to new structure
            fn = os.path.join('dict','et_fr.rst')
            logger.info("Generate %s",fn)
            fd = codecs.open(fn,'w','utf-8')
            write_header(fd,1,'eesti-prantsuse')
            t = SimpleTable(['Nr.',"ET","FR",u"hääldamine","Tasand"])
            self.words.sort(sort_by_et)
            words_et = [w for w in self.words if not w.hide_et]
            t.write(fd,[
                (i,w.et,html2rst(w.html_fr()),w.pronounciation,w.lesson.rst_ref_to()) 
                    for i,w in enumerate(words_et)])
            fd.close()

    def write_odt_file(self,target):
        from appy.pod.renderer import Renderer
        from lino.utils import iif
        from lino.utils.appy_pod import setup_renderer
        assert os.path.abspath(self.input_template) != os.path.abspath(target)
        if os.path.exists(target):
            os.remove(target)
        #~ tpl = os.path.join(os.path.dirname(__filename__),'cfr.odt')
        context = dict(
            self=self,
            iif=iif,
            )
        appy_params = dict()
        logger.info(u"appy.pod render %s -> %s (params=%s)",self.input_template,target,appy_params)
        renderer = Renderer(self.input_template, context, target,**appy_params)
        setup_renderer(renderer)
        #~ renderer.context.update(restify=debug_restify)
        renderer.run()
        
        
if USE_XHTML2ODT:

  class Book2(Book):
        
        
    def write_odt_file(self,target):
        #~ from lino.utils import iif
        #~ from lino.utils import AttrDict
        #~ from lino.utils.html2xhtml import html2xhtml
        
        assert os.path.abspath(self.input_template) != os.path.abspath(target)
        if os.path.exists(target):
            os.remove(target)
            
        options = AttrDict(
          url = "",
          template = self.input_template,
          output = target,
          with_network = True,
          verbose = True,
          top_header_level = 1,
          img_width = "8cm",
          img_height = "6cm",
          )
        
        #~ version=False # help="Show the version and exit")
        #~ input=input", metavar="FILE",
                          #~ help="Read the html from this file")
        #~ parser.add_option("-o", "--output", dest="output", metavar="FILE",
                          #~ help="Location of the output ODT file")
        #~ parser.add_option("-t", "--template", dest="template", metavar="FILE",
                          #~ help="Location of the template ODT file")
        #~ parser.add_option("-u", "--url", dest="url",
                          #~ help="Use this URL for relative links")
        #~ parser.add_option("-v", "--verbose", dest="verbose",
                          #~ action="store_true", default=False,
                          #~ help="Show what's going on")
        #~ parser.add_option("--html-id", dest="htmlid", metavar="ID",
                          #~ help="Only export from the element with this ID")
        #~ parser.add_option("--replace", dest="replace_keyword",
                          #~ default="ODT-INSERT", metavar="KEYWORD",
                          #~ help="Keyword to replace in the ODT template "
                          #~ "(default is %default)")
        #~ parser.add_option("--cut-start", dest="cut_start",
                          #~ default="ODT-CUT-START", metavar="KEYWORD",
                          #~ help="Keyword to start cutting text from the ODT "
                          #~ "template (default is %default)")
        #~ parser.add_option("--cut-stop", dest="cut_stop",
                          #~ default="ODT-CUT-STOP", metavar="KEYWORD",
                          #~ help="Keyword to stop cutting text from the ODT "
                          #~ "template (default is %default)")
        #~ parser.add_option("--top-header-level", dest="top_header_level",
                          #~ type="int", default="1", metavar="LEVEL",
                          #~ help="Level of highest header in the HTML "
                          #~ "(default is %default)")
        #~ parser.add_option("--img-default-width", dest="img_width",
                          #~ metavar="WIDTH", default="8cm",
                          #~ help="Default image width (default is %default)")
        #~ parser.add_option("--img-default-height", dest="img_height",
                          #~ metavar="HEIGHT", default="6cm",
                          #~ help="Default image height (default is %default)")
        #~ parser.add_option("--dpi", dest="img_dpi", type="int",
                          #~ default=96, metavar="DPI", help="Screen resolution "
                          #~ "in Dots Per Inch (default is %default)")
        #~ parser.add_option("--no-network", dest="with_network",
                          #~ action="store_false", default=True,
                          #~ help="Do not download remote images")
        #~ options, args = parser.parse_args()
        self.odtfile = MyODTFile(options)
        
        context = dict(iif=iif)
        context.update(book=self)
        self.odtfile.render(context)

    def as_odt(self):
        xhtml = ''.join([ln for ln in self.main.html_lines()])
        xhtml = html2xhtml(xhtml)
        #~ xhtml = "<div>%s</div>" % xhtml
        #~ xhtml = "<p>%s</p>" % xhtml
        #~ xhtml = '<html><body>%s</body></html>' % xhtml
        xhtml = '<html xmlns="http://www.w3.org/1999/xhtml"><body>%s</body></html>' % xhtml
        if not True:
            f = open("before.xml","wt")
            f.write(xhtml.encode('utf-8'))
            f.close()
        
        #~ logger.info("Gonna do it with %r",xhtml)
        xhtml = self.odtfile.xhtml_to_odt(xhtml)
        if True:
            f = open("after.xml","wt")
            f.write(xhtml)
            #~ f.write(xhtml.encode('utf-8'))
            f.close()
        return xhtml.decode('utf-8')
        
        
