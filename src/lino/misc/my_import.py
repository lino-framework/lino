def my_import(name):
	# http://www.python.org/doc/current/lib/built-in-funcs.html
	mod = __import__(name)
	# mod = __import__(name,globals(),locals(),[])
	components = name.split('.')
	for comp in components[1:]:
		mod = getattr(mod, comp)
	return mod

