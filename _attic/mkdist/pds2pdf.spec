# *-*-* python *-*-*

targets = ['pds2pdf','prn2pdf','publish']

def build:
a = Analysis([\
        os.path.join(HOMEPATH,'support','_mountzlib.py'),
        os.path.join(HOMEPATH,'support','useUnicode.py'),
        r'..\src\timtools\pds2pdf.py'],
        pathex=[])
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=1,
          name=os.path.join(BUILDPATH,'pds2pdf.exe'),
          debug=0,
          strip=0,
          console=1 )
coll = COLLECT( exe,
               a.binaries,
               strip=0,
               name=r'c:\temp\linodist')
