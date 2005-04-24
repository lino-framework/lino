#coding: latin1

## Copyright 2005 Luc Saffre.
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

import sys, os
import shutil
import stat
from time import strftime


try:
    import win32file
except:
    win32file = None


from lino.ui import console
from lino.misc.jobs import Task



## if gettext.find('lino')!=None:
##     gettext.translation('lino').install()
##     print "using language file ",gettext.find('dirssync')
## else:
##     print "no language file found."
##     _=lambda msg: msg
 



from lino.i18n import itr,_
itr("Start?",
   de="Arbeitsvorgang starten?",
   fr=u"Démarrer?")

itr("Counting directories...",
    de=u"Ordner zählen..."
    )
itr("Synchronize %s to %s",
    de=u"Synchronisiere %s nach %s")
itr("Source directory '%s' doesn't exist.",
    de="Ursprungsordner '%s' existiert nicht.")
itr("Found %d directories.",de="%d Ordner gefunden.")
itr("Overwrite newer target %s",
    de=u"Jüngere Zieldatei %s überschreiben")
itr("%s is up-to-date",de="%s ist unverändert")
itr("remove directory %s", de=u"Lösche Ordner %s")
itr("remove file %s",de=u"Lösche Datei %s")
itr("create directory %s",de="Erstelle Ordner %s")
itr("copy file %s to %s",de=u"Kopiere Datei %s nach %s")
itr("keep %d, update %d, copy %d, delete %d files.",
    de=u"%d belassen, %d+%d kopieren, %d löschen")
itr( "%d files and %d directories ",
     de="%d Dateien in %d Ordnern ",
     fr=u"%d fichiers das %d répertoires ")
     


itr("were removed",
    de="wurden gelöscht")
itr( "were updated", de="wurden aktualisiert")
itr("were copied", de=u"wurden kopiert")

itr("would have been removed", de=u"wären gelöscht worden")
itr("would have been updated", de="wären aktualisiert worden")
itr("would have been copied", de="wären kopiert worden")
itr("%d files up-to-date", de="%d Dateien unverändert")
        

#class SyncError(Exception):
#    pass

class SynchronizerTask(Task):
    
    def configure(self,src,target,simulate,showProgress):
        self.src = src
        self.target = target
        self.simulate = simulate
        self.showProgress = showProgress
        
        self.ignore_times = False
        self.modify_window = 2

        self.count_uptodate = 0
        self.count_delete_file = 0
        self.count_update_file = 0
        self.count_copy_file = 0
        self.count_delete_dir = 0
        self.count_update_dir = 0
        self.count_copy_dir = 0
        Task.configure(self)
        

    def getLabel(self):
        s = _("Synchronize %s to %s") % (self.src, self.target)
        if self.simulate:
            s += " (Simulation)"
        return s
    
    def start(self):
        if not os.path.exists(self.src):
            raise console.ApplicationError(
                _("Source directory '%s' doesn't exist."))

        if self.showProgress:
            self.status(_("Counting directories..."))
            n = 0
            for root, dirs, files in os.walk(self.src):
                n += len(dirs)
                n += len(files)
            self.status(_("Found %d directories.") % n)
            self.setMaxValue(n)
            
        if os.path.exists(self.target):
            #self.schedule(self.update,self.src,self.target)
            self.update_it(self.src,self.target)
        else:
            #self.schedule(self.copy,self.src,self.target)
            self.copy(self.src,self.target)


##     def purzel(self):
##         #self.job.inc()
##         pass
        
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

                
    def copy(self,src,target):
        self.job.increment()
        if os.path.isfile(src):
            self.copy_file(src,target)
        elif os.path.isdir(src):
            self.copy_dir(src,target)
        else:
            raise console.ApplicationError(
                "%s is neither file nor directory" % src)

    def update_it(self,src,target):
        self.job.increment()
        if os.path.isfile(src):
            self.update_file(src,target)
        elif os.path.isdir(src):
            self.update_dir(src,target)
        else:
            raise console.ApplicationError(
                "%s is neither file nor directory" % src)
        
    def delete(self,name):
        self.refresh()
        if os.path.isfile(name):
            self.delete_file(name)
        elif os.path.isdir(name):
            self.delete_dir(name)
        else:
            raise console.ApplicationError(
                "%s is neither file nor directory" % name)

            
    def update_dir(self,src,target):
        srcnames = os.listdir(src)
        destnames = os.listdir(target)
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

        if len(destnames) > 0 or len(mustCopy) > 0:
            self.count_update_dir += 1

        """
        why delete first?
        (1) disk space may be limited
        (2) if only upper/lowercase changed
        """
                
        for name in destnames:
            self.delete(os.path.join(target,name))
        del destnames

        for s,t in mustCopy:
            self.copy(s,t)
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
            self.error("os.stat() failed: ",e)
            return False

        doit = False
        if target_sz != src_sz:
            doit = True
        elif self.ignore_times:
            doit = False
        elif abs(target_mt - src_mt) > self.modify_window:
            doit = True
            if target_mt > src_mt:
                self.warning(_("Overwrite newer target %s")
                             %target)

        
        if not doit:
            self.count_uptodate += 1
            self.job.verbose(_("%s is up-to-date") % target)
            return
        self.count_update_file += 1
        if self.simulate:
            self.job.notice("update %s to %s" % (src,target))
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

        self.copy_file(src,target)

        if win32file:
            win32file.SetFileAttributesW(target, filemode)

        
            


    def copy_dir(self,src,target):
        self.count_copy_dir += 1
        self.job.notice(_("create directory %s") %target)
        if not self.simulate:
            try:
                os.mkdir(target)
            except OSError,e:
                self.error("os.mkdir('%s') failed",target)
                return
            self.utime(src,target)
            
        for fn in os.listdir(src):
##             self.schedule(self.copy,
##                           os.path.join(src,fn),
##                           os.path.join(target,fn))
            self.copy(os.path.join(src,fn),
                      os.path.join(target,fn))
        
    def copy_file(self,src,target):
        self.count_copy_file += 1
        self.job.notice(_("copy file %s to %s") % (src,target))
        if self.simulate:
            return
        try:
            shutil.copyfile(src, target)
        except IOError,e:
            self.error("copy_file('%s','%s') failed",src,target)
            return
        self.utime(src,target)

    def delete_dir(self,name):
        self.count_delete_dir += 1
        self.job.notice(_("remove directory %s") % name)
        if self.simulate:
            return
        
        for fn in os.listdir(name):
            self.delete(os.path.join(name,fn))
            
        try:
            os.rmdir(name)
        except IOError,e:
            self.error("os.rmdir('%s') failed",name)
            
    def delete_file(self,name):
        self.count_delete_file += 1
        self.job.notice(_("remove file %s") % name)
        if self.simulate:
            return

        if win32file:
            filemode = win32file.GetFileAttributesW(name)
            win32file.SetFileAttributesW(
                name, filemode & \
                ~win32file.FILE_ATTRIBUTE_READONLY & \
                ~win32file.FILE_ATTRIBUTE_HIDDEN & \
                ~win32file.FILE_ATTRIBUTE_SYSTEM)
        else:
            os.chmod(name, stat.S_IWUSR)

        try:
            os.remove(name)
        #except Exception,e:
        #    console.error(str(e))
        except IOError,e:
            self.error("os.remove('%s') failed",name)
            
    def summary(self):
        s = _("%d files and %d directories ")
        if self.simulate:
            s += _("would have been removed")
        else:
            s += _("were removed")
        self.job.notice(s,
                  self.count_delete_file,
                  self.count_delete_dir)
        
        s = _("%d files and %d directories ")
        if self.simulate:
            s += _("would have been updated")
        else:
            s += _("were updated")
        self.job.notice(s,
                  self.count_update_file,
                  self.count_update_dir,
                  )
        
        s = _("%d files and %d directories ")
        if self.simulate:
            s += _("would have been copied")
        else:
            s += _("were copied")
        self.job.notice(s,
                  self.count_copy_file,
                  self.count_copy_dir,
                  )
        
        self.job.notice(_("%d files up-to-date"),self.count_uptodate)
        Task.summary(self)

    def getStatus(self):
##         if self._done:
##             return "done"
##         if self._aborted:
##             return "aborted"
        s = _("keep %d, update %d, copy %d, delete %d files.") % (
            self.count_uptodate,
            self.count_update_file,
            self.count_copy_file,
            self.count_delete_file)
        return s + " " + Task.getStatus(self)

class Sync(console.ConsoleApplication):

    name="Lino/sync"
    years='2005'
    author='Luc Saffre'
    usage="usage: lino sync [options] SRC DEST"
    description="""\
where SRC and DEST are two directories to be synchronized.
""" 
    
    def setupOptionParser(self,parser):
        console.ConsoleApplication.setupOptionParser(self,parser)

        parser.add_option(
            "-s", "--simulate",
            help="simulate only, don't do it",
            action="store_true",
            dest="simulate",
            default=False)

        parser.add_option(
            "-p", "--progress",
            help="show progress bar",
            action="store_true",
            dest="showProgress",
            default=False)
    
    def applyOptions(self,options,args):
        console.ConsoleApplication.applyOptions(self,options,args)

        if len(args) != 2:
            raise console.UsageError("needs 2 arguments")
            #parser.print_help() 
            #return -1

        src = args[0]
        target = args[1]
    
        #src = os.path.normpath(src)
        #target = os.path.normpath(target)

        self.task = SynchronizerTask(
            src=src,
            target=target,
            simulate=options.simulate,
            showProgress=options.showProgress)

    def run(self,ui):
         
        if not self.task.simulate:
            if not ui.confirm(self.task.getLabel()+"\n"+_("Start?")):
                return
        
        self.task.run(ui)

##     for l in sync.summary():
##         console.notice(l)


# lino.runscript expects a name consoleApplicationClass
consoleApplicationClass = Sync

if __name__ == '__main__':
    consoleApplicationClass().main() # console,sys.argv[1:])
    
##     try:
##         sys.exit(main(sys.argv[1:]))
##         #main(sys.argv[1:])
##     except SyncError,e:
##         console.error(str(e))
##         sys.exit(-1)
        

