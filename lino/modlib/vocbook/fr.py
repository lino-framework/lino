# -*- coding: UTF-8 -*-
## Copyright 2011 Luc Saffre
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

from lino.utils.restify import restify
from lino.utils.rstgen import SimpleTable, write_header, html2rst

from lino.modlib.vocbook.base import Language, Word, WordType, pronunciationRE

PRONOMS = "je tu il nous vous ils".split()

class Autre(WordType): 
    pass

class Adjectif(WordType): 
    text = "adj."

class Verbe(WordType): 
    text = "v."

class Nom(WordType): 
    text = "s."
        
class NomGeographique(WordType):
    text = u"n.géogr."
    
class NomPropre(WordType):
    pass
    #~ text = u"n.p."
  
class Numerique(WordType):
    text = u"num."

class Expression(WordType):
    text = u"expr."



class FrenchWord(Word):
    partner = None
    defini = None
    haspire = None
    #~ et = None
    adjectif = None
    #~ children = None
    parent = None
    #~ hide_et = False
    
    def __init__(self,text,
        defini=None,
        haspire=False,
        parent=None,**kw):
        if parent: self.parent = parent
        if defini: self.defini = defini
        if haspire: self.haspire = haspire
        Word.__init__(self,text,**kw)
        
    def marry(self,w):
        if w.type == self.type:
            if not self.gender:
                self.gender = 'm'
            if w.gender:
                if self.gender != w.opposite_gender():
                    raise Exception("Cannot marry %s and %s (same gender)" % (self,w))
            else:
                w.gender = self.opposite_gender()
            self.partner = w
            w.partner = self
            if not self.gender:
                raise Exception("Cannot marry %s and %s (unknown gender)" % (self,w))
            return
            
        if not w.type:
            w.type = Adjectif
            
        if w.type == Adjectif:
            if self.adjectif:
                self.adjectif.marry(w)
            else:
                self.adjectif = w
            return
        raise Exception("Cannot marry %r and %r" % (self,w))
        



class French(Language):
  
    @classmethod
    def parse_word(cls,s,cl=None,**kw):
        s = s.strip()
        mo = pronunciationRE.match(s)
        if mo:
            s = mo.group(1).strip()
            kw.update(pronounciation=mo.group(2).strip())
        if s.startswith("le "): 
            s = s[3:]
            cl = Nom
            kw.update(gender='m',defini=True)
        if s.startswith("la "): 
            s = s[3:]
            cl = Nom
            kw.update(gender='f',defini=True)
        if s.startswith("un "): 
            s = s[3:]
            cl = Nom
            kw.update(gender='m',defini=False)
        if s.startswith("une "): 
            s = s[4:]
            cl = Nom
            kw.update(gender='f',defini=False)
            
        if s.startswith("les "): 
            s = s[4:]
            cl = Nom
            kw.update(gender='pl',defini=True)
            
        if s.startswith("l'"): 
            cl = Nom
            s = s[2:]
            kw.update(defini=True)
            
        if s.startswith("j'"): 
            cl = Verbe
            s = s[2:]
            kw.update(form=0)
            
        for form,p in enumerate(PRONOMS):
            if s.startswith(p+" "): 
                s = s[len(p)+1:]
                cl = Verbe
                kw.update(form=form)
            
        if s.startswith("*"):
            kw.update(haspire=True)
            s = s[1:]
            
        if s.endswith(" (m)"): 
            s = s[:-4]
            kw.update(gender='m')
            if cl is None: cl = Adjectif
              
        if s.endswith(" (f)"): 
            s = s[:-4]
            kw.update(gender='f')
            if cl is None: cl = Adjectif
              
        if s.endswith(" (mf)"): 
            s = s[:-5]
            kw.update(gender='mf')
            if cl is None: cl = Adjectif
              
        if cl:
            kw.update(type=cl)
            
        return cls.register_word(FrenchWord(s,**kw))
  

    @classmethod
    def word2html(cls,w):
        hfr = w.text
        if w.haspire:
            hfr = "*"+ hfr
        if w.gender:
            return u"<b>%s</b> (%s%s.)" % (hfr,w.type.text,w.gender)
        if w.type and w.type.text:
            return u"<b>%s</b> (%s)" % (hfr,w.type.text)
        return u"<b>%s</b>" % hfr
        

    @classmethod
    def present_word2html(cls,w,book):
        """
        Format word for "presentation" (usually the first column 
        in a table of new words).
        """
        hfr = w.text
        if w.haspire:
            hfr = "*"+ hfr
        if Verbe.is_of_this_type(w):
            if w.form is not None:
                return u"%s <b>%s</b>" % (PRONOMS[w.form],hfr)
        if Nom.is_of_this_type(w):
            if w.gender == 'pl':
                return u"les <b>%s</b>" % hfr
            if w.defini and (w.text[0].lower() in u'aeiouyàé' or (w.text[0].lower() == 'h' and not w.haspire)):
                return u"l'<b>%s</b> (%s)" % (hfr,w.gender)
            #~ art = w.get_article()
            #~ def get_article(self):
            if w.defini:
                articles = ['le','la']
            else:
                articles = ['un', 'une']
            if w.gender == 'm':
                return u"%s <b>%s</b>" % (articles[0],hfr)
            if w.gender == 'f':
                return u"%s <b>%s</b>" % (articles[1],hfr)
                
            return u"%s <b>%s</b>" % (articles[0],hfr)
            raise Exception("Unknown gender for Nom %s" % w)
        return cls.word2html(w)



            
