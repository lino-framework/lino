"""

"""
import os
from os.path import abspath, dirname
from suds.client import Client

url = abspath(dirname(__file__)).replace(os.path.sep,"/")
url += '/XSD/TestConnectionService.wsdl'
url = 'file:///' + url 
client = Client(url)
print client

