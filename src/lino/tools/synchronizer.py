# -*- coding: ISO-8859-1 -*-
## Copyright 2005-2007 Luc Saffre.
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

"""
20051207 new features:

multiple projects: each project is a couple of src-target
directories. The summary for the user takes all projects as a whole.

safe mode: first run all tasks with .simulate=True, then display
summaries and suggest:
- abort if warnings or errors
- otherwise do it

"""

import sys, os
import shutil
import stat
from fnmatch import fnmatch
from time import strftime



try:
    import win32file
except:
    win32file = None

from lino.i18n import itr,_
#from lino.console.application import ApplicationError
from lino.adamo.exceptions import OperationFailed
from lino.console.task import Progresser, Task

class NeitherFileNorDirectory(Exception): pass



## if gettext.find('lino')!=None:
##     gettext.translation('lino').install()
##     print "using language file ",gettext.find('dirssync')
## else:
##     print "no language file found."
##     _=lambda msg: msg
 



itr("Start?",
   de=u"Arbeitsvorgang starten?",
   fr=u"Démarrer?")
itr("%d target files are NEWER! Are you sure?",
    de=u"%d Zieldateien sind NEUER! Sind Sie sicher?",
    fr=u"%d fichiers cible sont plus récents! Etes-vous certain?")

itr("Counting files...",
    de=u"Dateien zählen..."
    )
itr("Analyzing %s ...",
    de=u"Analysiere %s ...",
    fr=u"Analyse de %s en cours ..."
    )
itr("Nothing to do",de="Nichts zu tun")
itr("Synchronizing %s ...",
    de=u"Synchronisiere %s ...",
    fr=u"Synchronisation de %s en cours ...",
    )
itr("Source directory '%s' doesn't exist.",
    de="Ursprungsordner '%s' existiert nicht.")
itr("Target directory '%s' doesn't exist.",
    de="Zielordner '%s' existiert nicht.")
itr("Found %d files.",de="%d Dateien gefunden.")
itr("Overwrite newer target %s",
    de=u"Jüngere Zieldatei %s überschreiben")
itr("%s is up-to-date",de=u"%s ist unverändert")
itr("Must remove %s", de=u"Ordner %s zu löschen")
itr("Must delete %s",de=u"Datei %s zu löschen")
itr("Must update %s",de=u"Datei %s zu aktualisieren")
itr("Removing %s", de=u"Lösche Ordner %s")
itr("Deleting %s", de=u"Lösche Datei %s")
itr("create directory %s",de="Erstelle Ordner %s")
#itr("copy file %s to %s",de=u"Kopiere Datei %s nach %s")
itr("Copying %s",de=u"Kopiere %s")
itr("Updating %s",de=u"Aktualisiere %s")

itr("keep %d, update %d (%d newer), copy %d, delete %d files.",
    de=u"%d gleich, %d aktualisieren (%d neuer), %d kopieren, %d löschen."
    )


itr("kept %d, updated %d, copied %d, deleted %d files.",
    de=u"%d gleich, %d aktualisiert, %d kopiert, %d gelöscht.")



itr( "%d files and %d directories ",
     de="%d Dateien und %d Ordner ",
     fr=u"%d fichiers et %d répertoires ")
     


itr("to remove",
    de=u"zu löschen")
itr("to update",
    de="zu aktualisieren")
itr("to copy",
    de="zu kopieren")
itr("were removed",
    de=u"wurden gelöscht")
itr( "were updated", de="wurden aktualisiert")
itr("were copied", de=u"wurden kopiert")

itr("would have been removed", de=u"wären gelöscht worden")
itr("would have been updated", de=u"wären aktualisiert worden")
itr("would have been copied", de=u"wären kopiert worden")
itr("%d files up-to-date", de=u"%d Dateien unverändert")
itr("%d files ", de="%d Dateien ")
        

class Synchronizer(Progresser):
    
    def __init__(self):
        Progresser.__init__(self)
        #Job.__init__(self)
        self.simulate=True
        self.count_errors = 0
        #self.count_warnings = 0
        self.count_newer = 0
        self.count_same = 0
        self.count_delete_file = 0
        self.count_update_file = 0
        self.count_copy_file = 0
        self.count_delete_dir = 0
        #self.count_update_dir = 0
        self.count_copy_dir = 0
        
        self.done_same = 0
        self.done_delete_file = 0
        self.done_update_file = 0
        self.done_copy_file = 0
        self.done_delete_dir = 0
        #self.done_update_dir = 0
        self.done_copy_dir = 0
        self.projects=[]

        self._statusAnalysing = _("keep %d, update %d (%d newer), "
                                  "copy %d, delete %d files.")
        
        self._statusDoing = _("kept %d, updated %d, copied %d,"
                              " deleted %d files.")

    def addProject(self,*args,**kw):
        prj=SyncProject(self,*args,**kw)
        self.projects.append(prj)
        


    def run(self,safely=True,noaction=False):
        #self.session=task.session
        #self.task=task
        #self.maxval=0
        #for p in self.projects:
        #    self.notice(str(p))
            
##         if showProgress:
##             def f():
##                 for prj in self.projects:
##                     self.maxval += prj.countFiles(self)
##             Looper(f,_("Counting files...")).runfrom(self)
##             #sess.loop(f,_("Counting files..."))
##             self.notice(_("Found %d files."), self.maxval)
            
                
        if safely:
            self.simulate=True
            
##             def f(task):
##                 for p in self.projects:
##                     task.runtask(p)
##             self.loop(f,_("Analyzing..."),self.maxval)

            for p in self.projects:
                self.notice(_("Analyzing %s ..."),p)
                self.runtask(p)
                p.setMaxVal(p.curval)
            
            self.notice(self.getSummary())
            
            if not (self.count_delete_dir \
                 or self.count_delete_file \
                 or self.count_copy_file \
                 or self.count_copy_dir \
                 or self.count_update_file) :
                self.notice(_("Nothing to do"))
                return
            
                    
            if self.count_newer > 0:
                if not self.confirm(
                    _("%d target files are NEWER! Are you sure?") \
                    % self.count_newer, default=False):
                    return
        else:
            self.notice(self.getSummary())
            
        if noaction:
            return

        if not self.confirm(_("Start?")):
            return
        
        self.simulate=False
        
##         def f(task):
##             for p in self.projects:
##                 task.runtask(p)
##         self.loop(f,"Synchronizing",self.maxval)

        for p in self.projects:
            self.notice(_("Synchronizing %s ..."),p)
            self.runtask(p)
        
        self.notice(self.getSummary())
        
                
##     def getLabel(self):
##         s = _("Synchronize %s to %s") % (self.src, self.target)
##         if self.simulate:
##             s += " (Simulation)"
##         return s


    def getStatus(self):
        if self.simulate:
            return self._statusAnalysing % (
                self.count_same,
                self.count_update_file,
                self.count_newer,
                self.count_copy_file,
                self.count_delete_file)
        else:
            return self._statusDoing % (
                self.done_same,
                self.done_update_file,
                self.done_copy_file,
                self.done_delete_file)
        #return s + " " + Job.getStatus(self)
            
##     def getStatusSynchronizing(self):
##         return s + " " + Job.getStatus(self)

    def getSummary(self):
        l=[]
        if self.count_same:
            l.append( _("%d files up-to-date") % self.count_same)
        if self.count_delete_file or self.count_delete_dir:
            s = _("%d files and %d directories ")
            if self.simulate:
                s += _("to remove")
            else:
                s += _("were removed")

            l.append(s % (self.count_delete_file,
                          self.count_delete_dir))
        
        #s = _("%d files and %d directories ")
        if self.count_update_file:
            s = _("%d files ")
            if self.simulate:
                s += _("to update")
            else:
                s += _("were updated")
            l.append(s % self.count_update_file)

        if self.count_copy_file or self.count_copy_dir:
            s = _("%d files and %d directories ")
            if self.simulate:
                s += _("to copy")
            else:
                s += _("were copied")
            l.append(s % (self.count_copy_file, self.count_copy_dir))
        
        #if self.count_newer:
        #l += Job.getSummary(self)
        return "\n".join(l)

    
    
#class SyncTask(Task):
class SyncProject(Progresser):
    
    #summaryClass=SyncSummary
    
    #def __init__(self,app,src,target,simulate,recurse,summary=None):
    def __init__(self,job,src,target,recurse=False,ignorePatterns=None):
        Progresser.__init__(self)
        #self.app=app
        self.job=job
        self.src = unicode(src)
        self.target = unicode(target)
        #self.simulate = simulate
        self.recurse = recurse
        self.ignorePatterns = ignorePatterns
        
        self.ignore_times = False        
        self.modify_window = 2

        if not os.path.exists(self.src) \
              and not os.path.ismount(self.src):
            raise OperationFailed(
                _("Source directory '%s' doesn't exist.") % self.src)

        if not os.path.exists(self.target) \
              and not os.path.ismount(self.target):
            raise OperationFailed(
                _("Target directory '%s' doesn't exist.") % self.target)

    def getStatus(self):
        return self.job.getStatus()
    
    def countFiles(self,ui):
        if self.recurse:
            n = 0
            for root, dirs, files in os.walk(self.src):
                # n += len(dirs)
                n += len(files)
                ui.breathe()
            return n
        return len(os.listdir(self.src))

    def __str__(self):
        s="sync '"+self.src+"' '"+self.target+"'"
        if self.recurse: s += " -r"
        return s

##     def doit(self,task):
##         self.task=task
##         self.update_dir(self.src,self.target)
        
    def run(self):
        return self.update_dir(self.src,self.target)


    def ignore(self,fn):
        if self.ignorePatterns is not None:
            for i in self.ignorePatterns:
                if fnmatch(fn,i): return True
        return False

        
    def update_dir(self,src,target):
        if self.ignore(src): return
        if self.ignore(target): return
##         if self.ignorePatterns is not None:
##             for i in self.ignorePatterns:
##                 if not fnmatch(src,i): return
##                 if not fnmatch(target,i): return
        srcnames = os.listdir(src)
        destnames = os.listdir(target)
        if self.ignorePatterns is not None:
            srcnames=[n for n in srcnames if not self.ignore(n)]
            destnames=[n for n in destnames if not self.ignore(n)]
        mustCopy = []
        mustUpdate = []
        for name in srcnames:
            s = os.path.join(src,name)
            t = os.path.join(target,name)
            try:
                destnames.remove(name)
            except ValueError:
                mustCopy.append( (s,t) )
            else:
                mustUpdate.append( (s,t) )

        #if len(destnames) > 0 or len(mustCopy) > 0:
        #    self.summary.count_update_dir += 1

        """
        why delete first?
        (1) disk space may be limited
        (2) if only upper/lowercase changed
        """
                
        for name in destnames:
            self.delete_it(os.path.join(target,name))
        del destnames

        for s,t in mustCopy:
            self.copy_it(s,t)
        del mustCopy
            
        for s,t in mustUpdate:
            self.update_it(s,t)

    
    def update_file(self,src,target):
        try:
            src_st = os.stat(src)
            src_sz = src_st.st_size
            src_mt = src_st.st_mtime
        except OSError,e:
            self.error("os.stat() failed: ",e)
            return False

        try:
            target_st = os.stat(target)
            target_sz = target_st.st_size
            target_mt = target_st.st_mtime
        except OSError,e:
            self.error("os.stat() failed: %s",e)
            return False

        doit = False
        if target_sz != src_sz:
            doit = True
        elif self.ignore_times:
            doit = False
        elif abs(target_mt - src_mt) > self.modify_window:
            doit = True
            if target_mt > src_mt:
                self.job.count_newer += 1
                self.warning(
                    _("Overwrite newer target %s") % target)

        
        if not doit:
            if self.job.simulate:
                self.job.count_same += 1
            else:
                self.job.done_same += 1
            self.debug(_("%s is up-to-date"), target)
            return
        
        if self.job.simulate:
            self.job.count_update_file += 1
            self.verbose("Must update %s", target)
            return
        
        if win32file:
            filemode = win32file.GetFileAttributesW(target)
            win32file.SetFileAttributesW(
                target,
                filemode & \
                ~win32file.FILE_ATTRIBUTE_READONLY & \
                ~win32file.FILE_ATTRIBUTE_HIDDEN & \
                ~win32file.FILE_ATTRIBUTE_SYSTEM)
        else:
            os.chmod(target, stat.S_IWUSR)

        #self.copy_file(src,target)

        self.verbose(_("Updating %s"),target)
        try:
            shutil.copyfile(src, target)
        except IOError,e:
            self.error("copyfile('%s','%s') failed",src,target)
            return
        
        self.utime(src,target)
        #self.job.done_copy_file += 1        

        if win32file:
            win32file.SetFileAttributesW(target, filemode)
            
        self.job.done_update_file += 1

        
            


    def copy_dir(self,src,target):
        if self.job.simulate:
            self.job.count_copy_dir += 1
        else:
            self.verbose(_("Creating directory %s"), target)
            try:
                os.mkdir(target)
            except OSError,e:
                self.error("os.mkdir('%s') failed",target)
                return
            # self.utime(src,target)
            self.job.done_copy_dir += 1

        srcnames=os.listdir(src)
        if self.ignorePatterns is not None:
            srcnames=[n for n in srcnames if not self.ignore(n)]
        
        for fn in srcnames:
            self.copy_it(os.path.join(src,fn),
                         os.path.join(target,fn))
        
    def copy_file(self,src,target):
        #self.verbose(_("copy file %s to %s") % (src,target))
        if self.job.simulate:
            self.verbose(_("Must copy %s"), target)
            self.job.count_copy_file += 1
            return
        #self.notice(_("copy file %s to %s") % (src,target))
        self.verbose(_("Copying %s"), target)
        try:
            shutil.copyfile(src, target)
        except IOError,e:
            self.error("copyfile('%s','%s') failed",src,target)
            return
        
        self.utime(src,target)
        self.job.done_copy_file += 1

    def delete_dir(self,name):
        if self.job.simulate:
            self.verbose(_("Must remove %s") % name)
            self.job.count_delete_dir += 1
            return
        
        self.verbose(_("Removing %s") % name)
        for fn in os.listdir(name):
            self.delete_it(os.path.join(name,fn))
            
        try:
            os.rmdir(name)
        except IOError,e:
            self.error("os.rmdir('%s') failed",name)
        self.job.done_delete_dir += 1
            
    def delete_file(self,name):
        if self.job.simulate:
            self.verbose(_("Must delete %s"),name)
            self.job.count_delete_file += 1
            return

        self.verbose(_("Deleting %s"),name)
        if win32file:
            filemode = win32file.GetFileAttributesW(name)
            try:
                win32file.SetFileAttributesW(
                    name, filemode & \
                    ~win32file.FILE_ATTRIBUTE_READONLY & \
                    ~win32file.FILE_ATTRIBUTE_HIDDEN & \
                    ~win32file.FILE_ATTRIBUTE_SYSTEM)
            except win32file.error,e:
                self.error(name+" : SetFileAttributesW() failed")
        else:
            os.chmod(name, stat.S_IWUSR)

        try:
            os.remove(name)
        #except Exception,e:
        #    console.error(str(e))
        except IOError,e:
            self.error("os.remove('%s') failed",name)
        self.job.done_delete_file += 1

##     def showStatus(self):
##         self.status(self.job.getStatus())
##         self.breathe()

    def error(self,*args,**kw):
        Progresser.error(self,*args,**kw)
        self.job.count_errors += 1
        
    #def warning(self,*args,**kw):

    def copy_it(self,src,target):
        #self.showStatus()
        self.breathe()
        self.job.increment()
        if os.path.isfile(src):
            self.copy_file(src,target)
        elif os.path.isdir(src):
            if self.recurse:
                self.copy_dir(src,target)
        else:
            raise NeitherFileNorDirectory(repr(src))
            #raise ApplicationError(
            #    "%s is neither file nor directory" % src)
            #self.task.abort(
            #    "%s is neither file nor directory" % src)

    def update_it(self,src,target):
        #self.showStatus()
        self.breathe()
        #self.setStatus()
        self.job.increment()
        if os.path.isfile(src):
            self.update_file(src,target)
        elif os.path.isdir(src):
            if self.recurse:
                self.update_dir(src,target)
        else:
            raise NeitherFileNorDirectory()
            #raise ApplicationError(
            #self.task.abort(
            #    "%s is neither file nor directory" % src)

        
    def delete_it(self,name):
        #self.setStatus()
        self.breathe()
        #self.showStatus()
        if os.path.isfile(name):
            self.delete_file(name)
        elif os.path.isdir(name):
            self.delete_dir(name)
        else:
            raise NeitherFileNorDirectory()
            #raise ApplicationError(
            #self.task.abort(
            #    "%s is neither file nor directory" % name)

            
            
            
    def utime(self,src,target):
        # Note: The utime api of the 2.3 version of python is
        # not unicode compliant.
        try:
            s = os.stat(src)
        except OSError,e:
            self.error("os.stat() failed: %s",e)
            return
        
        try:
            os.utime(target, (s.st_atime, s.st_mtime))
        except OSError,e:
            self.error("os.utime() failed: %s",e)

                
