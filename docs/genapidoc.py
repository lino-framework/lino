import os
OUTPUT_DIR = "api"
SOURCE_DIR = r"..\..\src"
cwd = os.getcwd()
os.chdir(OUTPUT_DIR)
for fn in os.listdir("."):
   (base,ext) = os.path.split(fn)
   if ext == '.html':
      os.remove(fn)
      
import pydoc
pydoc.writedocs(SOURCE_DIR)
os.chdir(cwd)
