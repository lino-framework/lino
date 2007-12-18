## Copyright 2007 Luc Saffre 

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


class MakeError(Exception):
    pass


class Song:
    def __init__(self,title=None,title2=None,
                 filename=None,width=None,
                 singable="",remark="", 
                 composer="", author="",
                 number=None,
                 soprano=None,
                 alto=None,
                 alto2=None,
                 tenor=None,
                 bass=None,
                 lyrics=None,
                 bass_lyrics=None,
                 soprano_lyrics=None,
                 alto_lyrics=None,
                 lead_voice=None,
                 ):
        
        self.title=title
        self.title2=title2
        self.filename=filename
        self.singable=singable
        self.remark=remark
        self.scorewidth=width
        self.composer=composer
        self.author=author
        self.soprano=soprano
        self.alto=alto
        self.alto2=alto2
        self.tenor=tenor
        self.bass=bass
        self.soprano_lyrics=soprano_lyrics
        self.alto_lyrics=alto_lyrics
        self.bass_lyrics=bass_lyrics
        self.number=number
        self.lyrics=lyrics
        self.lyrics_font="Helvetica" # AvantGarde, Palatino
        if lead_voice is None:
            lead_voice="soprano"
        self.lead_voice=lead_voice
        if width is not None:
            self.textwidth=180-width

        #self.inputfile=os.path.abspath(filename+".ly")
        # self.inputfile.replace("\\","/")
        #assert os.path.exists(self.inputfile)
        
    def __getitem__(self,name):
        return getattr(self,name)

    def has_music(self):
        return self.soprano
    def is_single_staff(self):
        return not self.bass

    def toLilypond(self,fd):

        if False and len(self.lyrics) > 1:
            fd.write(r"""
secondverse = \lyricmode {
            """ + self.lyrics[1] + " }")

        if self.is_single_staff():
            fd.write(r"""
\score{
            """)
            fd.write(self.soprano)
            if self.lyrics:
                fd.write(r"\addlyrics { " + self.lyrics + " }")

            fd.write(r"""
  \midi {}
  \layout {}
}

            """)
        else:
            #if self.soprano:
            #    fd.write("upperOne = " + self.soprano)
            if self.alto:
                fd.write("upperTwo =  " + self.alto)
            if self.tenor:
                fd.write("lowerOne =  " + self.tenor)
            if self.bass:
                fd.write("lowerTwo =  " + self.bass)

            #if self.lyrics:
            #    fd.write(r"firstverse = \lyricmode { " + self.lyrics + " }")
                
##             if self.alto2:
##                 fd.write(r"""
##                 voiceFive = #(context-spec-music (make-voice-props-set 4) 'Voice)
##                 """)
                
            fd.write(r"""
\score{ 

    \context StaffGroup<<

        \context Staff = "upper"
            """)
            
            fd.write(r"""
            <<
            \clef treble
            """)

            if self.soprano:
                fd.write(r"""
                \context Voice = "soprano" %(soprano)s
                """ % self)
            
            if self.alto:
                fd.write(r"""
                \context Voice = "alto" %(alto)s 
                """ % self)
            
            if self.alto2:
                fd.write(r"""
                \context Voice = "alto2" %(alto2)s 
                """ % self)
            
            fd.write(r"""
            >>
            
            """ % self)
            
            if self.soprano_lyrics:
                fd.write(r"""
        \lyricsto "soprano" \new Lyrics {
                    \set stanza = ""
                    \override LyricText  #'font-name = #"%(lyrics_font)s"
                    \lyricmode { %(soprano_lyrics)s }
                    }

                """ % self)
                
            if self.lyrics:
                fd.write(r"""
        \lyricsto "%(lead_voice)s" \new Lyrics {
                    \set stanza = ""
                    \override LyricText  #'font-name = #"%(lyrics_font)s"
                    \lyricmode { %(lyrics)s }
                    }

                """ % self)
            
            fd.write(r"""
            
        \context Staff = "lower" <<
                    
                    \clef bass
                    \context Voice = "tenor" \lowerOne
                    \context Voice = "bass" \lowerTwo
                    >>
            """)
            
            if self.bass_lyrics:
                fd.write(r"""
        \lyricsto "bass" \new Lyrics {
                    \set stanza = ""
                    \override LyricText  #'font-name = #"%(lyrics_font)s"
                    \lyricmode { %(bass_lyrics)s }
                    }

                """ % self)
            
            fd.write(r"""
        >>


\layout {

        \context{\Lyrics
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
        
        \context{\Score
        barNumberVisibility = #all-invisible
        }
    }

\midi { }
}
            """)
                    
        fd.write("""
\paper {
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
                    


    def toLytex(self,fd):
        
        if self.title2 is None:
            fd.write(r"""            
\subsection*{\framebox{\huge ~%(number)d~} %(title)s}
            """ % self)
        else:
            fd.write(r"""
\subsection*{\framebox{\huge ~%(number)d~} %(title)s \hfill {\small (%(title2)s)}}
            """ % self)

##         fd.write(r"""
## %%\begin{figure}[h]
## \marginpar{\framebox{Nr. %(number)d}}
## %%\end{figure}
##         """ % self)
        
            
        if self.has_music():
            if self.scorewidth is not None:
                fd.write(r"""
\begin{minipage}{%(scorewidth)dmm}
""" % self)
            if self.scorewidth is None:
                fd.write(r"""
\begin[noindent,staffsize=14]{lilypond}
""")
            else:
                fd.write(r"""
\begin[noindent,staffsize=14,line-width=%d\mm]{lilypond}
""" % self.scorewidth)
            
            self.toLilypond(fd)
            
            fd.write(r"""
\end{lilypond}""")
            if self.scorewidth is not None:
                fd.write(r"""
\end{minipage}\hfill
\begin{minipage}{%(textwidth)dmm}
""" % self)
                
        fd.write(r"""
\par\normalsize %(singable)s
\par\small  %(remark)s
        """ % self)

        if self.has_music():
            if self.scorewidth is not None:
                fd.write(r"""
\end{minipage}
""" % self)

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




class Songbook(Application):
    
    name="Lino Songbook"
    copyright="""\
Copyright (c) 2007 Luc Saffre.
This software comes with ABSOLUTELY NO WARRANTY and is
distributed under the terms of the GNU General Public License.
See file COPYING.txt for more information."""
    url=__url__+"/songbook.html"
    
    usage="usage: lino sng2pdf [options] FILES"
    description="""\
creates a songbook
where FILES is one or more files to be converted to a pdf file.
"""
    
    
    def __init__(self,filename,output_dir,
                 input_encoding=None):
        self.output_dir=output_dir
        self.filename=filename
        self.input_encoding=input_encoding
        self.songs = []
        Application.__init__(self)

    def addsong(self,*args,**kw):
        self.songs.append(Song(*args,**kw))

    def loadfile(self,filename,**kw):
        fd = codecs.open(filename,"r",self.input_encoding)
        for song in yaml.load_all(fd):
            song.update(kw)
            self.addsong(**song)
        fd.close()

    def loadsongs(self,songlist):
        for name in songlist.splitlines():
            name=name.strip()
            if len(name) != 0:
                fd = codecs.open(name+".sng","r",self.input_encoding)
                for songdict in yaml.load_all(fd):
                    songdict['filename']=name
                    songdict['number']=len(self.songs)+1
                    self.addsong(**songdict)
                fd.close()

    def write_lytex_file(self,filename):
        self.notice("Generating %s...",
                    os.path.join(self.output_dir,filename))
        fd = codecs.open(filename,"w","utf8")

        fd.write(r"""
        
%% \documentclass[12pt,smallheadings,halfparskip]{scrartcl}
\documentclass[12pt]{article}
% ATTENTION: THIS FILE HAS BEEN GENERATED BY 
% python laulud.py
%
% \usepackage{ngerman}
\usepackage[utf8]{inputenc}
\usepackage[a5paper,landscape,
    twoside,bindingoffset=5mm,
    heightrounded,
    left=10mm,right=10mm,top=10mm,bottom=10mm]{geometry}
%% \usepackage{picins} %% http://latex.tugraz.at/mpic.pdf
%% \usepackage{floatflt} %% http://www.fi.infn.it/pub/tex/doc/orig/floatflt.pdf
%% \usepackage{songbook}
\usepackage{helvet}
%% \usepackage{times}

\renewcommand{\familydefault}{\sfdefault}

%% \makeindex % tells LaTeX to write an .idx file
\setlength{\parindent}{0mm}
\begin{document}
        
        """)

        for song in self.songs:
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

        if False:
            for song in self.songs:
                pngfile=song.filename + ".png"
                lyfile=song.filename+".ly"
                if mustmake(pngfile,lyfile):
                    cmd="lilypond --png %s.ly" % song.filename
                    os.system(cmd)
                if mustmake(pngfile,lyfile):
                    raise MakeError(cmd)
            
        #texfile=os.path.join(tempdir,filename) + ".tex"
        #lytexfile=os.path.join(tempdir,filename) + ".lytex"
        #pdffile=os.path.join(tempdir,filename) + ".pdf"
        
        self.write_lytex_file(self.filename+".lytex")
        
        #cmd="lilypond-book.py --pdf %s.lytex" % filename
        #os.system(cmd)        
        retcode=os.spawnl(os.P_WAIT,sys.executable,sys.executable,LYBOOK,
                          "--pdf", self.filename+".lytex")
        if retcode != 0:
            raise MakeError(LYBOOK + " failed with exit code %d" % retcode)

        os.system("pdflatex " + self.filename+".tex")
##         retcode=os.spawnl(os.P_WAIT,PDFLATEX,"foo",filename+".tex")
##         if retcode != 0:
##             raise MakeError("pdflatex failed with exit code %d" % retcode)
        os.startfile(self.filename+".pdf")
        os.chdir(cwd)


    def setupOptionParser(self,parser):
        Application.setupOptionParser(self,parser)
    
        parser.add_option("-o", "--output",
                          help="""\
write to OUTFILE rather than FILE.pdf""",
                          action="store",
                          type="string",
                          dest="outFile",
                          default=None)
    
    def run(self):
        
        if self.options.outFile:
            path,filename = os.path.split(self.options.outFile)
            if len(path) != 0:
                self.output_dir=path
            name,ext=os.path.splitext(filename)
            if len(ext) != 0:
                assert ext.lower() == ".pdf"
            self.filename=name
            
        self.notice("Write %d songs to %s.pdf",
                    len(self.songs),
                    os.path.join(self.output_dir,self.filename))

        try:
            self.make()
        except MakeError, e:
            print e
            sys.exit(1)
        

            
def mustmake(target,*dependencies):
    if not os.path.exists(target):
        return True
    targettime=os.path.getmtime(target)
    for dep in dependencies:
        if os.path.getmtime(dep) > targettime:
            return True






## _SONGBOOK = Songbook()


## addsong = _SONGBOOK.addsong
## make = _SONGBOOK.make

## __all__ = ('addsong', 'make')

