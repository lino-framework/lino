# setup.py
from distutils.core import setup
import py2exe

setup(name="TIM Tools",
      scripts=["prn2pdf.py","itimi.py","sendmail.py"],
)

