#!/usr/bin/python

# Python conterpart of rsync written by Vivian De Smedt
# Send any comment or bug report to vivian@vdesmedt.com.
# I would like to thanks William Tan for its support in tuning rsync.py to support unicode path.

"""
changes LS:

20041129 : main() : (1) "--times" was still not correctly
recognized. (2) A (wrong) option "--time" was silently ignored, now
main() raises exception for any non-recognized option.

20050210 : 


"""

#from __future__ import nested_scopes

import os, os.path, shutil, glob, re, sys, getopt, stat, string


try:
    import win32file
except:
    win32file = None

class Cookie:
    def __init__(self):
        self.src_root = ""
        self.target_root = ""
        self.quiet = 0
        self.recursive = 0
        self.relative = 0
        self.dry_run = 0
        self.times = 0
        self.update = 0
        self.cvs_ignore = 0
        self.ignore_time = 0
        self.delete = 0
        self.delete_excluded = 0
        self.size_only = 0
        self.modify_window = 2
        self.existing = 0
        self.filters = []
        self.case_sensitivity = 0
        if os.name == "nt":
            self.case_sensitivity = re.I



def visit(cookie, dirname, names):
    """Copy files names from src_root + (dirname - src_root) to target_root + (dirname - src_root)"""

    print "visit(%s,%s)" % (dirname,names)
    
    if os.path.split(cookie.src_root)[1]:
        # Should be tested with
        # (C:\Cvs -> C:\)!
        # (C:\Archives\MyDatas\UltraEdit -> C:\Archives\MyDatas)
        # (Cvs -> "")!
        # (Archives\MyDatas\UltraEdit -> Archives\MyDatas)
        # (\Cvs -> \)! 
        # (\Archives\MyDatas\UltraEdit -> Archives\MyDatas)
        dirname = dirname[len(cookie.src_root) + 1:]
    else:
        dirname = dirname[len(cookie.src_root):]
        
    target_dir = os.path.join(cookie.target_root, dirname)
    if not os.path.isdir(target_dir):
        makeDir(cookie, target_dir)
    src_dir = os.path.join(cookie.src_root, dirname)

    filters = []
    if cookie.cvs_ignore:
        ignore = os.path.join(src_dir, ".cvsignore")
        if os.path.isfile(ignore):
            filters = convertPatterns(ignore, "-")
    filters = filters + cookie.filters

    if filters:
        # filter src files (names):
        name_index = 0
        while name_index < len(names):
            name = names[name_index]
            path = os.path.join(dirname, name)
            path = convertPath(path)
            if os.path.isdir(os.path.join(src_dir, name)):
                path = path + "/"
            for filter in filters:
                if re.search(filter[1], path, cookie.case_sensitivity):
                    if filter[0] == '-':
                        src = os.path.join(src_dir, name)
                        if cookie.delete_excluded:
                            if os.path.isfile(src):
                                removeFile(cookie, src)
                            elif os.path.isdir(src):
                                removeDir(cookie, src)
                            else:
                                logError("Src %s is neither a file nor a folder (skip removal)" % src)
                        del(names[name_index])
                        name_index = name_index - 1
                    elif filter[0] == '+':
                        break
            name_index = name_index + 1

    if cookie.delete:
        # Delete files and folder in target not present in filtered src.
        for name in os.listdir(target_dir):
            if not name in names:
                target = os.path.join(target_dir, name)
                if os.path.isfile(target):
                    removeFile(cookie, target)
                elif os.path.isdir(target):
                    removeDir(cookie, target)
                else:
                    pass

    for name in names:
        # Copy files and folder from src to target.
        src = os.path.join(src_dir, name)
        #print src
        target = os.path.join(target_dir, name)
        if os.path.exists(target):
            if os.path.isfile(src):
                if os.path.isfile(target):
                    # file-file
                    if shouldUpdate(cookie, src, target):
                        updateFile(cookie, src, target)
                elif os.path.isdir(target):
                    # file-folder
                    removeDir(cookie, target)
                    copyFile(cookie, src, target)
                else:
                    # file-???
                    logError("Target %s is neither a file nor folder (skip update)" % src)

            elif os.path.isdir(src):
                if os.path.isfile(target):
                    # folder-file
                    removeFile(cookie, target)
                    makeDir(cookie, target)
            else:
                # ???-xxx
                logError("Src %s is neither a file nor a folder (skip update)" % src)

        elif not cookie.existing:
            if os.path.isfile(src):
                copyFile(cookie, src, target)
            elif os.path.isdir(src):
                makeDir(cookie, target)
            else:
                logError("Src %s is neither a file nor a folder (skip update)" % src)


def log(cookie, message):
    if not cookie.quiet:
        try:
            print message
        except UnicodeEncodeError:
            print message.encode("utf8")


def logError(message):
    try:
        sys.stderr.write(message + "\n")
    except UnicodeEncodeError:
        sys.stderr.write(message.encode("utf8")+"\n")


def shouldUpdate(cookie, src, target):
    try:
        src_st = os.stat(src)
        src_sz = src_st.st_size
        src_mt = src_st.st_mtime
    except:
        logError("Fail to retrieve information about src %s (skip update)" % src)
        return 0

    try:
        target_st = os.stat(target)
        target_sz = target_st.st_size
        target_mt = target_st.st_mtime
    except:
        logError("Fail to retrieve information about target %s (skip update)" % target)
        return 0

    if cookie.update:
        return target_mt < src_mt - cookie.modify_window

    if cookie.ignore_time:
        return 1

    if target_sz != src_sz:
        return 1

    if cookie.size_only:
        return 0

    if abs(target_mt - src_mt) > cookie.modify_window:
##         print "%s to %s:\nabs(%s - %s) > %s" % (
##             src,target,
##             target_mt, src_mt,
##             cookie.modify_window)
        return 1
    return 0


def copyFile(cookie, src, target):
    log(cookie, "copy: %s to: %s" % (src, target))
    if cookie.dry_run:
        return
    try:
        shutil.copyfile(src, target)
        utime(cookie,src,target)
    except:
        logError("Failed to copy %s" % src)
    

def utime(cookie,src,target):
    # never called if dry_run
    # Note: The utime api of the 2.3 version of python is
    # not unicode compliant.    
    if cookie.times:
        try:
            s = os.stat(src)
            os.utime(target, (s.st_atime, s.st_mtime))
            print "os.utime(%s,%s,%s)" % (
                target, s.st_atime, s.st_mtime)
        except:
            logError("Failed to copy timestamp of %s" % src)


def updateFile(cookie, src, target):
    log(cookie, "update: %s to: %s" % (src, target))
    if cookie.dry_run:
        return
    # Read-only, hidden and system files cannot be overwritten.
    try:
        try:
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
        except:
            raise
            #logError("Fail to allow override of %s" % target)
            #pass
        

        shutil.copyfile(src, target)
        utime(cookie,src,target)

    except:
        logError("Failed to overwrite %s" % src)

    if win32file:
        win32file.SetFileAttributesW(target, filemode)


def removeFile(cookie, target):
    # Read only files could not be deleted.
    log(cookie, "remove: %s" % target)
    if not cookie.dry_run:
        try:
            try:
                if win32file:
                    filemode = win32file.GetFileAttributesW(target)
                    win32file.SetFileAttributesW(
                        target, filemode & \
                        ~win32file.FILE_ATTRIBUTE_READONLY & \
                        ~win32file.FILE_ATTRIBUTE_HIDDEN & \
                        ~win32file.FILE_ATTRIBUTE_SYSTEM)
                else:
                    os.chmod(target, stat.S_IWUSR)
            except:
                #logError("Fail to allow removal of %s" % target)
                pass

            os.remove(target)
        except:
            logError("Fail to remove %s" % target)



def makeDir(cookie, target):
    log(cookie, "make dir: %s" % target)
    if not cookie.dry_run:
        try:
            os.makedirs(target)
        except:
            logError("Fail to make dir %s" % target)


def removeDir(cookie, target):
    # Read only directory could not be deleted.
    log(cookie, "remove dir: %s" % target)
    if not cookie.dry_run:
        try:
            # 20041129 why ignore errors?
            # shutil.rmtree(target,True)
            shutil.rmtree(target) #, True)
        except Exception,e:
            logError("Fail to remove dir %s : %s" % (target,str(e)))


def convertPath(path):
    # Convert windows, mac path to unix version.
    separator = os.path.normpath("/")
    if separator != "/":
        path = re.sub(re.escape(separator), "/", path)

    # Help file, folder pattern to express that it should match the all file or folder name.
    path = "/" + path
    return path


def convertPattern(pattern, sign):
    """Convert a rsync pattern that match against a path to a filter that match against a converted path."""

    # Check for include vs exclude patterns.
    if pattern[:2] == "+ ":
        pattern = pattern[2:]
        sign = "+"
    elif pattern[:2] == "- ":
        pattern = pattern[2:]
        sign = "-"

    # Express windows, mac patterns in unix patterns (rsync.py extension).
    separator = os.path.normpath("/")
    if separator != "/":
        pattern = re.sub(re.escape(separator), "/", pattern)

    # If pattern contains '/' it should match from the start.
    temp = pattern
    if pattern[0] == "/":
        pattern = pattern[1:]
    if temp[-1] == "/":
        temp = temp[:-1]

    # Convert pattern rules: ** * ? to regexp rules.
    pattern = re.escape(pattern)
    pattern = string.replace(pattern, "\\*\\*", ".*")
    pattern = string.replace(pattern, "\\*", "[^/]*")
    pattern = string.replace(pattern, "\\*", ".*")

    if "/" in temp:
        # If pattern contains '/' it should match from the start.
        pattern = "^\\/" + pattern
    else:
        # Else the pattern should match the all file or folder name.
        pattern = "\\/" + pattern

    if pattern[-2:] != "\\/" and pattern[-2:] != ".*":
        # File patterns should match also folders.
        pattern = pattern + "\\/?"

    # Pattern should match till the end.
    pattern = pattern + "$"
    return (sign, pattern)


def convertPatterns(path, sign):
    """Read the files for pattern and return a vector of filters"""
    filters = []
    f = open(path, "r")
    while 1:
        pattern = f.readline()
        if not pattern:
            break
        if pattern[-1] == "\n":
            pattern = pattern[:-1]

        if re.match("[\t ]*$", pattern):
            continue
        if pattern[0] == "#":
            continue
        filters = filters + [convertPattern(pattern, sign)]
    f.close()
    return filters


def printUsage():
    """Print the help string that should printed by rsync.py -h"""
    print "usage: rsync.py [options] source target"
    print """
 -q, --quiet              decrease verbosity
 -r, --recursive          recurse into directories
 -R, --relative           use relative path names
 -u, --update             update only (don't overwrite newer files)
 -t, --times              preserve times
 -n, --dry-run            show what would have been transferred
     --existing           only update files that already exist
     --delete             delete files that don't exist on the sending side
     --delete-excluded    also delete excluded files on the receiving side
 -I, --ignore-times       don't exclude files that match length and time
     --size-only          only use file size when determining if a file should
                          be transferred
     --modify-window=NUM  timestamp window (seconds) for file match (default=2)
     --existing           only update existing target files or folders
 -C, --cvs-exclude        auto ignore files in the same way CVS does
     --exclude=PATTERN    exclude files matching PATTERN
     --exclude-from=FILE  exclude patterns listed in FILE
     --include=PATTERN    don't exclude files matching PATTERN
     --include-from=FILE  don't exclude patterns listed in FILE
     --version            print version number
 -h, --help               show this help screen

See http://www.vdesmedt.com/~vds2212/rsync.html for informations and updates.
Send an email to vivian@vdesmedt.com for comments and bug reports."""


def printVersion():
    print "rsync.py version 1.0.8"


def main(argv):
    cookie = Cookie()

    opts, args = getopt.getopt(argv, "qrRntuCIh", ["quiet", "recursive", "relative", "dry-run", "times", "update", "cvs-ignore", "ignore-times", "help", "delete", "delete-excluded", "existing", "size-only", "modify-window=", "exclude=", "exclude-from=", "include=", "include-from=", "version"])
    for o, v in opts:
        if o in ["-q", "--quiet"]:
            cookie.quiet = 1
        elif o in ["-r", "--recursive"]:
            cookie.recursive = 1
        elif o in ["-R", "--relative"]:
            cookie.relative = 1
        elif o in ["-n", "--dry-run"]:
            cookie.dry_run = 1
        elif o in ["-t", "--times"]:
            cookie.times = 1
        elif o in ["-u", "--update"]:
            cookie.update = 1
        elif o in ["-C", "--cvs-ignore"]:
            cookie.cvs_ignore = 1
        elif o in ["-I", "--ignore-time"]:
            cookie.ignore_time = 1
        elif o == "--delete":
            cookie.delete = 1
        elif o == "--delete-excluded":
            cookie.delete = 1
            cookie.delete_excluded = 1
        elif o == "--size-only":
            cookie.size_only = 1
        elif o == "--modify-window":
            cookie.modify_window = int(v)
        elif o == "--existing":
            cookie.existing = 1
        elif o == "--exclude":
            cookie.filters = cookie.filters + [convertPattern(v, "-")]
        elif o == "--exclude-from":
            cookie.filters = cookie.filters + convertPatterns(v, "-")
        elif o == "--include":
            cookie.filters = cookie.filters + [convertPattern(v, "+")]
        elif o == "--include-from":
            cookie.filters = cookie.filters + convertPatterns(v, "+")
        elif o == "--version":
            printVersion()
            return 0
        elif o in ["-h", "--help"]:
            printUsage()
            return 0
        else:
            raise "unrecognized option " + str(o)

    if len(args) <= 1:
        printUsage()
        return 1

    #print cookie.filters

    target_root = args[1]
    try: # In order to allow compatibility below 2.3.
        # pass # removed by LS 20050210
        if os.path.supports_unicode_filenames:
            target_root = unicode(target_root,
                                  sys.getfilesystemencoding())
    finally:
        cookie.target_root = target_root

    srcs = glob.glob(args[0])
    if not srcs:
        return 0

    if cookie.relative:
        cookie.src_root = ""
    else:
        cookie.src_root = src_root

    # new LS 20050211:
    for src in srcs:
        pfn = os.path.join(cookie.src_root, src)
        if src.endswith(os.path.sep):
            visit(cookie,pfn,os.listdir(pfn))
        elif os.path.isfile(pfn):
            files.append(pfn)
        else:
            visit(cookie,pfn,os.listdir(pfn))

    if len(files):
        assert not self.delete, ""
        visit(
            
        if cookie.recursive:
                os.path.walk(pfn, visit, cookie)
    return 0

    

##     src_families = {}
##     for src in srcs:
##         try: 
##             if os.path.supports_unicode_filenames:
##                 src = unicode(src, sys.getfilesystemencoding())
##         except:
##             pass
        
##         src_name = ""
##         src_root = src
##         while not src_name:
##             src_root, src_name = os.path.split(src_root)
##         if not src_families.has_key(src_root):
##             src_families[src_root] = []
##         src_families[src_root] = src_families[src_root] \
##                                    + [ src_name ]

##     for src_root in src_families.keys():
##         if cookie.relative:
##             cookie.src_root = ""
##         else:
##             cookie.src_root = src_root

##         global y # In order to allow compatibility below 2.1 (nested scope was used before).
        
##         y = src_root
##         files = filter(lambda x: os.path.isfile(os.path.join(y, x)),
##                        src_families[src_root])
##         if files:
##             visit(cookie, src_root, files)

##         y = src_root
##         folders = filter(lambda x: os.path.isdir(os.path.join(y, x)),
##                          src_families[src_root])
##         for folder in folders:
##             folder_path = os.path.join(src_root, folder)
##             if not cookie.recursive:
##                 def f(x):
##                     return os.path.isfile(os.path.join(folder_path,x))
##                 files = filter(f, os.listdir(folder_path))
##                 visit(cookie, folder_path,files)
##             else:
##                 os.path.walk(folder_path, visit, cookie)
##     return 0

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
