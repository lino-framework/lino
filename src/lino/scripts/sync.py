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

class SyncError(Exception):
    pass

class Synchronizer:
    def __init__(self,simulate):
        self.simulate=simulate
        #self.logger = logger
        
        self.ignore_times = False
        self.modify_window = 2

        self.count_uptodate = 0
        self.count_delete_file = 0
        self.count_update_file = 0
        self.count_copy_file = 0
        self.count_delete_dir = 0
        self.count_update_dir = 0
        self.count_copy_dir = 0

        self.job = console.progress("Synchronizer")
 


    def mustUpdate(self, src, target):
        try:
            src_st = os.stat(src)
            src_sz = src_st.st_size
            src_mt = src_st.st_mtime
        except OSError,e:
        #except Exception,e:
            console.error("os.stat('%s') failed"%src)
            return False

        try:
            target_st = os.stat(target)
            target_sz = target_st.st_size
            target_mt = target_st.st_mtime
        except OSError,e:
        #except Exception,e:
            console.error("os.stat('%s') failed" % target)
            #console.error(str(e))
            return False

        if target_sz != src_sz:
            return True

        if self.ignore_times:
            return True

        if abs(target_mt - src_mt) > self.modify_window:
    ##         print "%s to %s:\nabs(%s - %s) > %s" % (
    ##             src,target,
    ##             target_mt, src_mt,
    ##             cookie.modify_window)
            return True
        
        return False


    def purzel(self):
        self.job.inc()
        
    def utime(self,src,target):
        # Note: The utime api of the 2.3 version of python is
        # not unicode compliant.    
        try:
            s = os.stat(src)
        except OSError,e:
        #except Exception,e:
            console.error("os.stat('%s') failed" % src)
            return
        
        try:
            os.utime(target, (s.st_atime, s.st_mtime))
        except OSError,e:
        #except Exception,e:
            console.error("os.utime('%s') failed" % target)

                
    def copy(self,src,target):
        self.purzel()
        if os.path.isfile(src):
            self.copy_file(src,target)
        elif os.path.isdir(src):
            self.copy_dir(src,target)
        else:
            raise SyncError(
                "%s is neither file nor directory" % src)

    def update(self,src,target):
        self.purzel()
        if os.path.isfile(src):
            self.update_file(src,target)
        elif os.path.isdir(src):
            self.update_dir(src,target)
        else:
            raise SyncError(
                "%s is neither file nor directory" % src)
        
    def delete(self,name):
        self.purzel()
        if os.path.isfile(name):
            self.delete_file(name)
        elif os.path.isdir(name):
            self.delete_dir(name)
        else:
            raise SyncError(
                "%s is neither file nor directory" % name)

##     def make_dir(self,name):
##         if self.simulate:
##             print "mkdir "+name
##             return
##         try:
##             os.makedirs(name)
##         except Exception,e:
##             console.error(str(e))
            
    def update_dir(self,src,target):
        self.count_update_dir += 1
        #srcdir = os.path.join(self.srcroot,dirname)
        #destdir = os.path.join(self.destroot,dirname)
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
                
        for name in destnames:
            self.delete(os.path.join(target,name))
        del destnames

        for s,t in mustCopy:
            self.copy(s,t)
        del mustCopy
            
        for s,t in mustUpdate:
            self.update(s,t)

    
    def update_file(self,src,target):
        if not self.mustUpdate(src,target):
            self.count_uptodate += 1
            self.vmsg(target+" is up-to-date")
            return
        self.count_update_file += 1
        self.message("update %s %s" % (src,target))
        if self.simulate:
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
        self.message("copy_dir %s to %s" % (src,target))
        if not self.simulate:
            try:
                os.mkdir(target)
            except OSError,e:
                console.error("os.mkdir('%s') failed" % target)
                return
            self.utime(src,target)
            
        for fn in os.listdir(src):
            self.copy(os.path.join(src,fn),
                      os.path.join(target,fn))
        
    def copy_file(self,src,target):
        self.count_copy_file += 1
        self.message("copy_file %s to %s" % (src,target))
        if self.simulate:
            return
        try:
            shutil.copyfile(src, target)
        except IOError,e:
            console.error("copyfile('%s','%s') failed" % (
                src,target))
            return
        self.utime(src,target)

    def delete_dir(self,name):
        self.count_delete_dir += 1
        self.message("rmdir "+name)
        if self.simulate:
            return
        
        for fn in os.listdir(name):
            self.delete(os.path.join(name,fn))
            
        try:
            os.rmdir(name)
        except IOError,e:
            console.error("os.rmdir('%s') failed" % name)
            
    def delete_file(self,name):
        self.count_delete_file += 1
        self.message("delete_file %s" % name)
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
            console.error("os.remove('%s') failed" % name)
        
    def summary(self):
        self.message("deleted %d directories and %d files" % (
            self.count_delete_dir,
            self.count_delete_file))
        self.message("updated %d directories and %d files" % (
            self.count_update_dir,
            self.count_update_file))
        self.message("copied %d directories and %d files" % (
            self.count_copy_file,
            self.count_copy_dir))
        self.message("%d files were up-to-date" % (
            self.count_uptodate))

    def vmsg(self,msg):
        console.vmsg(msg)

    def message(self,msg):
        console.message(msg)

def main(argv):
    console.copyleft(name="Lino/sync",
                     years='2005',
                     author='Luc Saffre')
    
    parser = console.getOptionParser(
        usage="usage: lino sync [options] SRC DEST",
        description="""\
where SRC and DEST are two directories to be synchronized.
""" )
    
    parser.add_option("-s", "--simulate",
                      help="""\
simulate only, don't do it""",
                      action="store_true",
                      dest="simulate",
                      default=False)
    (options, args) = parser.parse_args(argv)

    if len(args) != 2:
        parser.print_help() 
        sys.exit(-1)

    src = args[0]
    target = args[1]
    
    #src = os.path.normpath(src)
    #target = os.path.normpath(target)

    sync = Synchronizer(simulate=options.simulate)

    if not os.path.exists(src):
        raise SyncError(src+" doesn't exists")

    msg = "sync %s to %s\n" % (src,target)
    if sync.simulate:
        msg += "simulate it?"
    else:
        msg += "do it?"
        
    if not console.confirm(msg):
        return
        
    if os.path.exists(target):
        sync.update(src,target)
    else:
        sync.copy(src,target)

    sync.summary()

    sync.job.done()


if __name__ == '__main__':
    try:
        main(sys.argv[1:])
    except SyncError,e:
        console.error(str(e))
        sys.exit(-1)
        

