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


from lino.utils.restify import restify
from lino.utils.rstgen import SimpleTable, write_header, html2rst
from lino.utils import htmlgen
from lino.utils import uca_collator

pronunciationRE=re.compile("^(.*)\s*(\[.*\])\s*",re.DOTALL)


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
        return html2rst('<b>%s</b>' % w.text) + ' ' + w.get_pron_html()
        
class GEOF(GEOM):
    label = u'omadussõna (n)'
    gender = 'f'



#~ def mycmp(a,b):
    #~ return locale.strcoll(a,b)
        
def sort_by_fr(a,b):
    return locale.strcoll(a.text.lower(),b.text.lower())
    #~ return locale.strcoll(S(a.fr),S(b.fr))
    

class Section:
    def __init__(self,
            parent,number,title=None,intro=None,
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
        self.number = number
        self.title = title
        self.intro = intro
        self.body = []
        self.words = []
        self.children = []
        self.current_lesson = None
        
    def add_section(self,*args,**kw):
        sect = Section(self,*args,**kw)
        self.children.append(sect)
        return sect
        
    def add_index(self,*args,**kw):
        sect = Index(self,*args,**kw)
        self.children.append(sect)
        return sect
        
    def add_lesson(self,*args,**kw):
        self.current_lesson = Unit(self,len(self.children)+1,*args,**kw)
        self.children.append(self.current_lesson)

    def add_after(self,chunk):
        self.current_lesson.body.append(chunk)
        
    def parse_words(self,cl,lines):
        self.current_lesson.parse_words(cl,lines)
        
    def rst_ref_to(self):
        parts = self.name_parts()
        number = str(self.number)
        p = self.parent
        while p is not None:
            if p.number is not None:
                parts = ['%02d' % p.number] + parts
                number = str(p.number) + "." + number
            p = p.parent
        return ':doc:`%s </%s>`' % (number,'/'.join(parts))
        
    def html_ref_to(self):
        parts = self.name_parts()
        number = str(self.number)
        p = self.parent
        while p is not None:
            if p.number is not None:
                parts = ['%02d' % p.number] + parts
                number = str(p.number) + "." + number
            p = p.parent
        #~ return ':doc:`%s </%s>`' % (number,'/'.join(parts))
        return str(number)
        
    #~ def get_name_parts(self):
        #~ name = [,'index']
        #~ if self.parent is None:
            #~ return name
        #~ return self.parent.get_name_parts() + name
        #~ return self.parent.get_name_parts() + [self]
        
    def html_lines(self,level=1):
        if self.number is None:
            title = self.title
        else:
            title = "%s %s" % (self.html_ref_to(),self.title)
        yield htmlgen.H(level,title)
        
        if self.intro:
            yield htmlgen.restify(self.intro)
            
        for chunk in self.body:
            yield htmlgen.restify(chunk)
        
        if self.children:
            for s in self.children:
                for ln in s.html_lines(level+1):
                    yield ln
        
    def name_parts(self):
        if self.number is None:
            return ['index' ]
        else:
            if self.children:
                return [ '%02d' % self.number, 'index' ]
            else:
                return [ "%02d" % self.number ]
      
        
    def write_rst_files(self,root):
        #~ if self.number is not None:
            #~ name_parts = name_parts + 
            #~ leafname = 
        #~ fn = os.path.join('lessons','%02d.rst' % self.number)
        #~ fn = os.path.join(['%02d' % s.number for s in self.get_name_parts()]
        #~ fn = os.path.join(self.get_name_parts())
        #~ fn = os.path.join(root,*name_parts)
        #~ fn = root
        fn = os.path.join(root,*self.name_parts()) + ".rst"
        #~ if self.number is None:
            #~ fn = os.path.join(fn,'index')
        #~ else:
            #~ if self.children:
                #~ root = os.path.join(root,'%02d' % self.number)
                #~ fn = os.path.join(fn,'%02d' % self.number,'index')
            #~ else:
                #~ fn = os.path.join(fn,"%02d" % self.number)
          
        #~ fn += '.rst'
        logger.info("Generate %s",fn)
        newroot = os.path.dirname(fn)
        makedirs_if_missing(newroot)
        fd = codecs.open(fn,'w','utf-8')
        if self.number is None:
            write_header(fd,1,"%s" % self.title)
        else:
            #~ write_header(fd,1,"%d. %s" % (self.number,self.title))
            write_header(fd,1,"%s %s" % (self.html_ref_to(),self.title))
        self.write_body(fd)
        fd.close()
        for s in self.children:
            s.write_rst_files(newroot)

    def write_body(self,fd):
        if self.intro:
            fd.write(self.intro + '\n\n')
            
        for chunk in self.body:
            fd.write(chunk + '\n\n')
        

        if self.children:
            fd.write("""\
.. toctree::
   :maxdepth: 2
   
""")
            for s in self.children:
                fd.write("   "  + ("/".join(s.name_parts())) + "\n")
            fd.write('\n\n')




class Unit(Section):
    columns = [FR,PRON,ET]
    def __init__(self,parent,number,title,intro=None,
            after=None,
            columns=None,show_headers=None):
        if columns is not None:
            self.columns = columns
            if show_headers is None:
                show_headers = True
        elif show_headers is None:
            show_headers = False
        self.show_headers = show_headers
        self.parent = parent
        if not title:
            title = u"Leçon %d" % number
        Section.__init__(self,parent,number,title,intro)
        self.after = after
        self.words = []
        
    #~ def add_word(self,w):
        #~ self.words.append(w)
        
    def tablerow(self,w):
        return [col.render(w,self) for col in self.columns]
          
    def parse_words(self,cl,lines):
        #~ lesson = self.current_lesson
        for ln in lines.splitlines():
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
        if self.after:
            yield restify(self.after)
            
    def write_body(self,fd):
      
        Section.write_body(self,fd)
        
        #~ t = SimpleTable(["FR",u"hääldamine","ET"])
        
        words = [w for w in self.words if w.parent is None]
        #~ words = [w for w in self.book.words if self in w.lessons and w.parent is None]
        if words:
            t = SimpleTable([col.label for col in self.columns],
                    show_headers=self.show_headers)
            t.write(fd,[self.tablerow(w) for w in words])
          
            #~ t.write(fd,[(
                        #~ html2rst(w.html_fr()),
                        #~ w.pronounciation,
                        #~ w.et) for w in words])
        #~ else:
            #~ logger.warning("No words in %r",self.title)
        if self.after:
            fd.write('\n\n' + self.after + '\n\n')
            


def uca_sort(l):
    c = uca_collator()
    def k(w): return c.sort_key(w.text)
    l.sort(key=k)

  
  
            
            
            
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
            + ", ".join([u.html_ref_to() for u in w.units])
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
                


class Book:
    def __init__(self,from_language,to_language,title=None):
        self.main = Section(None,None,title,from_language=from_language,to_language=to_language)

    def add_section(self,*args,**kw):
        return self.main.add_section(*args,**kw)
        
    def add_index(self,*args,**kw):
        return self.main.add_index(*args,**kw)
        
    def html(self):
        #~ s = '\n'.join([ln for ln in self.main.html_lines()])
        s = htmlgen.DIV(self.main.html_lines)
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

    def write_odt_file(self,tpl,target):
        from appy.pod.renderer import Renderer
        from lino.utils import iif
        from lino.utils.appy_pod import setup_renderer
        #~ tpl = os.path.join(os.path.dirname(__filename__),'cfr.odt')
        context = dict(
            self=self,
            iif=iif,
            )
        appy_params = dict()
        logger.info(u"appy.pod render %s -> %s (params=%s)",tpl,target,appy_params)
        renderer = Renderer(tpl, context, target,**appy_params)
        setup_renderer(renderer)
        #~ renderer.context.update(restify=debug_restify)
        renderer.run()
        