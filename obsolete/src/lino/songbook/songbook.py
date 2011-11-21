## Copyright 2007-2008 Luc Saffre 

## This file is part of the Lino project.

## Lino is free software; you can redistribute it and/or modify it
## under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 2 of the License, or
## (at your option) any later version.

## Lino is distributed in the hope that it will be useful, but WITHOUT
## ANY WARRANTY; without even the implied warranty of MERCHANTABILITY
## or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public
## License for more details.

## You should have received a copy of the GNU General Public License
## along with Lino; if not, write to the Free Software Foundation,
## Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307 USA


import sys
import os
import codecs
import yaml

from lino import __url__
from lino.console.application import Application, UsageError

LYBOOK=r'"C:\Program Files\LilyPond\usr\bin\lilypond-book.py"'

PDFLATEX=r'"C:\Program Files\MiKTeX 2.5\miktex\bin\pdflatex.exe"'



# barNumberVisibility = #all-invisible



class MakeError(Exception):
    pass

class MyOptionDict:
    allowedAttribs=None
    def __init__(self,*args,**kw):
        self._attribs={}
        self.update(*args,**kw)
        
    def __getitem__(self,name):
        return self.__getattr__(name)


    def __repr__(self):
        l=[]
        for k,v in self._attribs.items():
            s=repr(v)
            if len(s) > 10:
                s=s[:4]+"..."+s[-4:]
            l.append(k+"="+s)
        return self.__class__.__name__+"("+",".join(l)+")"
    

    def __getattr__(self,name):
        try:
            return self._attribs[name]
        except KeyError:
            if self.allowedAttribs is not None:
                try:
                    return self.allowedAttribs[name]
                except KeyError:
                    pass
            raise AttributeError(
                "%s instance has no attribute '%s'" % (
                self.__class__.__name__, name))
    
    def update(self,*args,**kw):

        for a in args:
            if self.allowedAttribs is not None:
                if not a in self.allowedAttribs.keys():
                    raise AttributeError("No attribute '%s' in %s" % (a,self.__class__.__name__))
                assert type(True) == type(self.allowedAttribs[a])
            self._attribs[a]=True
            
        for k,v in kw.items():
            if self.allowedAttribs is not None:
                if not k in self.allowedAttribs.keys():
                    raise AttributeError("No attribute '%s' in %s" % (k,self.__class__.__name__))
                assert self.allowedAttribs[k] is None or type(v) == type(self.allowedAttribs[k])
            self._attribs[k]=v
    
    def remove(self,*args):
        for a in args:
            del self._attribs[a]
            
class PackageOptions(MyOptionDict):
    def __str__(self):
        l=[]
        for k,v in self._attribs.items():
            if v == True:
                l.append(k)
            elif type(v) == type(""):
                l.append(k+"="+v)
            elif type(v) == type([]):
                l.append(k+"={"+",".join(v)+"}")
        return ",".join(l)


class DocumentOptions(PackageOptions):
    pass
    
class GeometryOptions(PackageOptions):
    "http://www.tug.org/teTeX/tetex-texmfdist/doc/latex/geometry/geometry.pdf"
    pass


class Publication(MyOptionDict):
    allowedAttribs=dict(
        title=None,
        author=None,
        year=None)
        
class Book(Publication):
    allowedAttribs = dict(
        Publication.allowedAttribs,
        isbn=None,
        publisher=None)



class Section(MyOptionDict):
    allowedAttribs=dict(
        title=None,
        title2=None,
        filename=None,
        number=None,
        language=None,
        text=None,
        remark=None, 
        verses=None,
        versesColumns=None,
        versesWidth=None,
        newLines=None,
        mtime=None,
        )
        
    def __init__(self,sbk,**kw):
        self.sbk=sbk
        MyOptionDict.__init__(self,**kw)
        #print self.verses
        if self.title is not None:
            if self.number is None:
                self.update(number=sbk.songCounter + 1)
        if self.number is not None:
            if sbk.numbering:
                sbk.songCounter=self.number
                            

##     def __str__(self):
##         return self.title
        
    def has_music(self):
        return False
    
    def toLytex(self,fd):
        self.writeTitle(fd)
        self.writeBody(fd)
        
    def writeBody(self,fd):
        if self.text:
            fd.write(self.text)
        if self.verses:
            if self.versesColumns > 1:
                fd.write(r"""
\begin{multicols}{%d}""" % self.versesColumns)
            if not self.versesWidth:
                fd.write(r"""
\begin{enumerate}""")
            i=0
            for verse in self.verses:
                verse=verse.strip().replace("\n",self.newLines)
                i += 1
                if self.versesWidth:
                    fd.write(r"""
\begin{minipage}{%s}
  (%d) %s
\end{minipage}
""" % (self.versesWidth,i,verse))
                else:
                    fd.write(r"""
\item\parbox[t]{\linewidth}{""" +  verse + r"}")
##                     fd.write(r"""
## \item """ +  verse + r"\vfill")
                        
            if not self.versesWidth:
                    fd.write(r"""
\end{enumerate}""")
            if self.versesColumns > 1:
                fd.write(r"""
\vfill\end{multicols}""")
        s=""
        if self.textAuthor:
            s += "Text: " + self.textAuthor 
            if self.textYear:
                s += " (" + str(self.textYear) + ")"
            s += ". "
        if self.composedBy:
            s += "Music: " + self.composedBy 
            if self.composedYear:
                s += " (" + str(self.composedYear) + ")"
            s += ". "
        if self.arrangedBy:
            s += "Arr.: " + self.arrangedBy 
            if self.arrangedYear:
                s += " (" + str(self.arrangedYear) + ")"
            s += ". "
        if self.copyright:
            s += r"{\copyright}~" + self.copyright + ". "
        if self.remark: s += self.remark 
        if len(s) > 0:
            fd.write(r"""
\par\small  %s""" % s)

    
    def writeTitle(self,fd):
        
        if self.title:
            fd.write(r"""
\subsection*{ """)
            if self.number and self.sbk.numbering:
                fd.write(r"\framebox{\Huge ~%d~}~ " % self.number)
            fd.write(self.title)
            if self.title2:
                fd.write(r" \hfill {\small (%s)}" % self.title2)
            fd.write(r" }")

##         fd.write(r"""
## %%\begin{figure}[h]
## \marginpar{\framebox{Nr. %(number)d}}
## %%\end{figure}
##         """ % self)
        
            
class Song(Section):
    
    allowedAttribs = dict(
        Section.allowedAttribs,
        width=None,
        scorewidth=None,
        textwidth=None,
        singable=None,
        composedBy=None,
        composedYear=None,
        arrangedBy=None,
        arrangedYear=None,
        textAuthor=None,
        textYear=None,
        basedOn=None,
        soprano=None,
        alto=None,
        alto2=None,
        tenor=None,
        bass=None,
        lyrics=None,
        bassLyrics=None,
        sopranoLyrics=None,
        altoLyrics=None,
        lyricsFont="Arial", # Helvetica,AvantGarde, Palatino
        leadVoice="soprano",
        midiSuffixes=None,
        tempo=None,
        url=None,
        staffSize=None,
        copyright=None,
        bibliography=None,
        )
    
    def __init__(self,sbk,**kw):
        Section.__init__(self,sbk,**kw)
        if self.width is not None and self.textwidth is None:
            self.update(scorewidth=self.width,
                        textwidth=180-self.width)
            
        if self.newLines is None:
            self.update(newLines=sbk.newLines)
            
        if self.versesColumns is None:
            self.update(versesColumns=sbk.versesColumns)
        if self.midiSuffixes is None:
            l=[]
            if self.soprano: l.append("s")
            if self.alto: l.append("a")
            if self.tenor: l.append("t")
            if self.bass: l.append("b")
            if len(l) > 1:
                l.append("".join(l))
            self.update(midiSuffixes=l)
        if self.lyrics and type(self.lyrics) != type([]):
            self.lyrics = [ self.lyrics ]
        if self.staffSize is None:
            self.staffSize=sbk.staffSize

    def has_music(self):
        return self.soprano
    def is_single_staff(self):
        return not self.bass

    def toLilypond(self,fd):

        fd.write(r'''
\version "2.10.25"''')
        
        fd.write(r"""
%% http://lilypond.org/doc/v2.10/Documentation/user/lilypond/Style-sheets#Style-sheets        
\layout{
  \context { \Score
    \override MetronomeMark #'extra-offset = #'(-9 . 0)
    \override MetronomeMark #'padding = #'3
    \override BarNumber #'transparent = ##t   %% hide bar numbers
  }

  \context{\Lyrics
    \override LyricText  #'font-name = #"%(lyricsFont)s"
    \override VerticalAxisGroup #'minimum-Y-extent = #'(-0.5 . 3)

  }   
            
  \context{\StaffGroup
    \remove "Span_bar_engraver"
  }

  \context{\Staff
        \override VerticalAxisGroup #'minimum-Y-extent = #'(-3 . 3)
        autoBeaming = ##t
        \unset melismaBusyProperties 
        }
}

""" % self)
        fd.write(r"""
\score{ """)
        
        if not self.is_single_staff():

            fd.write(r"""
    \context StaffGroup <<
            """)
            
        if self.sopranoLyrics:
            fd.write(r"""
\new Lyrics = "soprano" { s1 }
%% http://lilypond.org/doc/v2.10/Documentation/user/lilypond/Vocal-ensembles
""")
            
        fd.write(r"""
        \new Staff = "upper"
            """)
        
        fd.write(r"""
        <<
        \clef treble
        """)
        
                
        if self.soprano:
            if self.tempo and self.sbk.showTempi:
                fd.write(r" { \tempo %s " % self.tempo)
            fd.write(r' \new Voice = "soprano" %s ' % self.soprano)
            if self.tempo and self.sbk.showTempi:
                fd.write(r" } ")

        if self.sopranoLyrics:
            fd.write(r"""
\context Lyrics = "soprano"
\lyricsto "soprano"
{
  \set stanza = ""
  \lyricmode { %(sopranoLyrics)s }
} """ % self)
            
        if self.alto:
            if self.tempo and self.sbk.showTempi:
                fd.write(r" { \tempo %s " % self.tempo)
            fd.write(r' \context Voice = "alto" %s ' % self.alto)
            if self.tempo and self.sbk.showTempi:
                fd.write(r" } ")
                

        if self.altoLyrics:
            fd.write(r"""
        \lyricsto "alto" \new Lyrics {
                    \set stanza = ""
                    \lyricmode { %(altoLyrics)s }
                    } """ % self)
                
        if self.lyrics:
            for lyrics in self.lyrics:
                fd.write(r"""
        \lyricsto "%s" \new Lyrics {""" % self.leadVoice)
                fd.write(r"""
\set stanza = "" """)
##                 fd.write(r"""
## \override LyricText  #'font-name = #"%s" """ % self.lyricsFont)
                fd.write(r"""
                    \lyricmode { %s }
                    } """ % lyrics)

        if not self.is_single_staff():
            fd.write(r"""
            >>
            """ % self)
            
            fd.write(r"""
            
        \new Staff = "lower" <<
                    
                    \clef bass """)
            if self.tenor:
                fd.write(r"""
                    \context Voice = "tenor" %(tenor)s """ % self)
            
            if self.bass:
                fd.write(r"""
                    \context Voice = "bass" %(bass)s """ % self)
                fd.write(r"""
                    >>
            """)
            
            if self.bassLyrics:
                fd.write(r"""
        \lyricsto "bass" \new Lyrics {
                    \set stanza = ""
                    \lyricmode { %(bassLyrics)s }
                    }""" % self)
            
        fd.write(r" >> """)
            
        fd.write(r"""
} %% end \score""") 
                    
        fd.write("""
\paper {
       between-system-padding = #0.1
       between-system-space = #0.1
       ragged-last-bottom = ##f
       ragged-bottom = ##f
       
%  myStaffSize = #20
%  #(define fonts
%    (make-pango-font-tree "Helvetica"
%                          "Helvetica"
%                          "Luxi Mono"
%                           (/ myStaffSize 20)))
%
%   %line-width = 6\in 
%   line-width = 19\cm 
%   indent = 0
%   pagenumber = "no"
  indent=0\mm
  line-width=180\mm
  oddFooterMarkup=##f
  oddHeaderMarkup=##f
  bookTitleMarkup = ##f
  scoreTitleMarkup = ##f
}

            """)
                    


    def writeBody(self,fd):
        if self.has_music():
            if self.scorewidth is not None:
                fd.write(r"""
\begin{minipage}{%(scorewidth)dmm}
""" % self)
            lilypondOptions=['noindent']
            if self.staffSize is not None:
                lilypondOptions.append('staffsize=%d' % self.staffSize)
            if self.scorewidth is not None:
                lilypondOptions.append(r'line-width=%s\mm' % self.scorewidth)
                
            fd.write(r"""
\begin[%s]{lilypond}""" % ",".join(lilypondOptions))
            
            self.toLilypond(fd)
            
            fd.write(r"""
\end{lilypond}""")
            if self.scorewidth is not None:
                fd.write(r"""
\end{minipage}\hfill
\begin{minipage}{%(textwidth)dmm}
""" % self)
        if self.singable:
            fd.write(r"""
\nopagebreak\normalsize %s""" % self.singable)

        Section.writeBody(self,fd)
        if self.has_music() and self.scorewidth is not None:
            fd.write(r"""
\end{minipage}""" % self)

            #~ %% \begin{samepage}
            #~ %% \begin{floatingfigure}{%(scorewidth)dmm}
            #~ %% \parpic[l]{
            #~ %% \begin{figure}
            #~ %% \bigskip
            #~ %% }
            #~ %% \end{floatingfigure}
            #~ %% \end{figure}
            #~ %% \picskip{0}
            #~ %% \end{samepage}

    def make_midi(self):
        for suffix in self.midiSuffixes:
            must_make=True
            midifile=self.filename + "_" + suffix + ".midi"
            lyfile=self.filename + "_" + suffix+".ly"
            if os.path.exists(midifile):
                if self.mtime < os.path.getmtime(midifile):
                    print "%s is up-to-date." % midifile
                    must_make=False
                else:
                    os.remove(midifile)
            if must_make:
                fd = codecs.open(lyfile,"w","utf8")
                self.toMidi(fd,suffix)
                fd.close()            
                cmd="lilypond --no-print %s" % lyfile
                print cmd
                os.system(cmd)
                if not os.path.exists(midifile):
                    raise MakeError(midifile)
            
    def toMidi(self,fd,suffix):
        """

        http://lilypond.org/doc/v2.10/Documentation/user/lilypond/MIDI-instruments#MIDI-instruments
        
        http://www.midistudio.com/Help/GMSpecs_Patches.htm
        
        """

        fd.write(r'\version "2.10.25"')
                
        fd.write(r"""
\score{
<<
""")
        
        if self.tempo:
            tempoString=r"\tempo " + self.tempo
        else:
            tempoString=""
            
        if self.soprano and "s" in suffix:
            fd.write(r"""
\new Staff {
  %s
  \set Staff.midiInstrument = "acoustic grand"
  %s
}""" % (tempoString,self.soprano))
            
        if self.alto and "a" in suffix:
            fd.write(r"""
\new Staff {
  %s
  \set Staff.midiInstrument = "acoustic guitar (nylon)"
  %s
}""" % (tempoString,self.alto))

        if self.tenor and "t" in suffix:
            fd.write(r"""
\new Staff {
  %s
  \set Staff.midiInstrument = "french horn"
  %s
}""" % (tempoString,self.tenor))

        if self.bass and "b" in suffix:
            fd.write(r"""
\new Staff {
  %s
  \set Staff.midiInstrument = "acoustic bass"
  %s
}""" % (tempoString,self.bass))

        fd.write(r"""
>>
\midi { }
}""")
                    


class Songbook(Application,MyOptionDict):
    
    name="Lino Songbook"
    copyright="""\
Copyright (c) 2007 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url=__url__+"/songbook.html"
    
    usage="usage: %s [options]" % sys.argv[0]

    allowedAttribs = dict(
        showFirstVerses=False,
        copyright=None,
        numbering=True,
        newLines=r" \\ ",
        filename=None,
        input_encoding=None,
        versesColumns=3,
        versesWidth=None,
        documentClass="article",
        output_dir=None,
        showTempi=True,
        staffSize=16,
        )
    
    def __init__(self,
                 geometryOptions=None,
                 documentOptions=None,
                 songnames=None,
                 **kw):
        
        Application.__init__(self)
        
        if geometryOptions is None: geometryOptions={}
        if documentOptions is None: documentOptions={}
        self.documentOptions=DocumentOptions(**documentOptions)
        self.geometryOptions=GeometryOptions(**geometryOptions)
        self.songCounter=0
        self.songs = []
        
        
        MyOptionDict.__init__(self,**kw)
        
        assert self.output_dir is not None

        if self.filename is None:
            basename,ext = os.path.splitext(sys.argv[0])
            self.update(filename=basename)
        
        if songnames is not None:
            self.loadsongs(songnames)
            
    def __getitem__(self,name):
        return getattr(self,name)

    def addsong(self,*args,**kw):
        self.songs.append(Song(self,*args,**kw))

    def addtext(self,**kw):
        self.songs.append(Section(self,**kw))

    def get_description(self):
        return """
Creates a songbook in directory %s.
Consisting of a pdf file and several midi files for each song.
If arguments are specified, then only these songs are included.

""" % self.output_dir
        
##     def loadfile(self,filename,**kw):
##         fd = codecs.open(filename,"r",self.input_encoding)
##         for song in yaml.load_all(fd):
##             song.update(kw)
##             self.addsong(**song)
##         fd.close()

    def loadsong(self,name,**kw):
        sngfile=name+".sng"
        fd = codecs.open(sngfile,"r",self.input_encoding)
        try:
            for songdict in yaml.load_all(fd):
                for k in songdict.keys():
                    if k.startswith(";"):
                        del songdict[k]
                songdict.update(kw)
                songdict['filename']=name
                songdict['mtime']=os.path.getmtime(sngfile)
                self.addsong(**songdict)
        except Exception,e:
            raise MakeError(sngfile+":"+str(e))
        fd.close()


    def loadsongs(self,songnames,**kw):
        for name in songnames.split():
            self.loadsong(name,**kw)

    def write_lytex_file(self,filename):
        self.notice("Generating %s...",
                    os.path.join(self.output_dir,filename))
        fd = codecs.open(filename,"w","utf8")

        fd.write(r"""
%% file generated by lino.songbook
\documentclass[%(documentOptions)s]{%(documentClass)s}""" % self)
        fd.write(r"""
% \usepackage{ngerman}
\usepackage[utf8]{inputenc}""")

        fd.write(r"""
\usepackage[%s]{geometry}""" % self.geometryOptions)
                 
        fd.write(r"""
%% \usepackage{picins} %% http://latex.tugraz.at/mpic.pdf
%% \usepackage{floatflt} %% http://www.fi.infn.it/pub/tex/doc/orig/floatflt.pdf
%% \usepackage{songbook}
\usepackage{multicol}
\usepackage{helvet}
%% \usepackage{arial}
%% \usepackage{times}

\pagestyle {empty}

\renewcommand{\familydefault}{\sfdefault}

%% \makeindex % tells LaTeX to write an .idx file
\setlength{\parindent}{0mm}
\parskip6pt
\begin{document}
        
        """)

        for song in self.songs:
            if len(self.args) == 0 or song.filename in self.args:
                song.toLytex(fd)

        fd.write("""
%% \printindex
\end{document}
        """)

        fd.close()

    def make(self):
        # see also:
        # http://griddlenoise.blogspot.com/2007/04/pythons-make-rake-and-bake-another-and.html
        assert not "/" in self.filename, "only basename"
        assert not "." in self.filename, "only basename"
        cwd = os.getcwd()
        os.chdir(self.output_dir)

        if "midi" in self.options.make:

            for song in self.songs:
                if len(self.args) == 0 or song.filename in self.args:
                    # print "midi:", song
                    if song.has_music():
                        song.make_midi()


        if "pdf" in self.options.make:
            
            if os.path.exists(self.filename+".pdf"):
                os.remove(self.filename+".pdf")

            self.write_lytex_file(self.filename+".lytex")

            retcode=os.spawnl(os.P_WAIT,sys.executable,sys.executable,LYBOOK,
                              "--pdf", self.filename+".lytex")
            if retcode != 0:
                raise MakeError(LYBOOK + " failed with exit code %d" % retcode)

            os.system("pdflatex " + self.filename+".tex")
    ##         retcode=os.spawnl(os.P_WAIT,PDFLATEX,PDFLATEX,self.filename+".tex")
    ##         if retcode != 0:
    ##             raise MakeError("pdflatex failed with exit code %d" % retcode)
            if not os.path.exists(self.filename+".pdf"):
                raise MakeError("File %s.pdf has not been created." % self.filename)
            os.startfile(self.filename+".pdf")
        os.chdir(cwd)

##     def mtime(self):
##         return os.path.getmtime(sys.argv[0])

    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-m", "--make",
                          help="""\
make only this type of files (midi or pdf)""",
                          action="store",
                          type="string",
                          dest="make",
                          default="midi,pdf")
    
    def run(self):

        
##         if self.options.outFile:
##             path,filename = os.path.split(self.options.outFile)
##             if len(path) != 0:
##                 self.output_dir=path
##             name,ext=os.path.splitext(filename)
##             if len(ext) != 0:
##                 assert ext.lower() == ".pdf"
##             self.filename=name

            
        if len(self.args) == 0:
            what= "all"
        else:
            what=str(len(self.args))
            
        self.notice("Write %s songs (%s) to %s.pdf...", 
            what, self.options.make,
            os.path.join(self.output_dir,self.filename))
        

        try:
            self.make()
        except MakeError, e:
            print e
            sys.exit(2)
        

            
## def mustmake(target,*dependencies):
##     if not os.path.exists(target):
##         return True
##     targettime=os.path.getmtime(target)
##     for dep in dependencies:
##         if os.path.getmtime(dep) > targettime:
##             return True






## _SONGBOOK = Songbook()


## addsong = _SONGBOOK.addsong
## make = _SONGBOOK.make

## __all__ = ('addsong', 'make')

