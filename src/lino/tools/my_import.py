import imp

def my_import(name):
	# http://www.python.org/doc/current/lib/built-in-funcs.html
	mod = __import__(name)
	# mod = __import__(name,globals(),locals(),[])
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod


def module_exists(full_name,path=None):
    """
    tests whether the module exists but does not import it.
    see http://www.python.org/doc/current/library/imp.html#module-imp
    """
    a = full_name.split('.',1)
    if len(a) == 1:
        # simple module name without package
        try:
            (file, pathname, description) = imp.find_module(full_name,path)
            if file is not None: file.close()
        except ImportError,e:
            return False
        return True
    assert len(a) == 2
    (file, pathname, description) = imp.find_module(a[0],path)
    if description[-1] != imp.PKG_DIRECTORY:
        return False
    pkg = imp.load_module(a[0],file,pathname,description)
    if file is not None: file.close()
    return module_exists(a[1],pkg.__path__)
