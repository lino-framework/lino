import os

# Caching directory lister, outputs (filelist,dirlist) tuple.
# If modification time of the directory is different, re-read directory.
# If it's the same, return cached contents.
# Based upon dircache.py

_listdir_cache = {}

def listdir(path):
	try:
		cached_mtime, files, directories = _listdir_cache[path]
		del _listdir_cache[path]
	except KeyError:
		cached_mtime, files, directories = -1, [], []
	try:
		mtime = os.stat(path).st_mtime
	except os.error:
		return []
	if mtime <> cached_mtime:
		try:
			list = os.listdir(path)
		except os.error:
			return []
		files=[]
		directories=[]
		for e in list:
			if os.path.isdir(os.path.join(path,e)):
				directories.append(e)
			else:
				files.append(e)
	_listdir_cache[path] = mtime, files, directories
	return files,directories

