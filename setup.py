#~ import os
import setuptools
#~ execfile(os.path.join('lino','setup_info.py'))
execfile('lino/setup_info.py')
def main(): setuptools.setup(**SETUP_INFO)
if __name__ == "__main__": main()
