a = Analysis([r's:\installer\support\_mountzlib.py', r's:\installer\support\useUnicode.py', 
r'..\src\timtools\prn2pdf.py'],
             pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name='build/prn2pdf.exe',
          debug=0,
          strip=0,
          console=1 )
coll = COLLECT( exe,
               a.binaries,
               strip=0,
               name=r'c:\temp\linodist')
