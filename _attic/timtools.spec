a = Analysis([
  's:\\installer\\support\\_mountzlib.py',
  's:\\installer\\support\\useUnicode.py',
  'prn2pdf.py',
  'itimi.py'],
  pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='buildstools/stools.exe',
          debug=0,
          strip=0,
          console=1 )
coll = COLLECT( exe,
               a.binaries,
               strip=0,
               name='diststools')
