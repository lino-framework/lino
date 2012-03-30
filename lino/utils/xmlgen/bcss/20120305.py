"""

"""
import os
from os.path import abspath, dirname
from suds.client import Client

service = 'TestConnectionService'
#~ service = 'RetrieveTIGroupsV3'

url = abspath(dirname(__file__)).replace(os.path.sep,"/")
url += '/XSD/%s.wsdl' % service
url = 'file:///' + url 
suds_options = dict()
#~ suds_options.update(location="")
client = Client(url,**suds_options)
print client
print "Sending request ..."
result = client.service.sendTestMessage("hello cbss service")
print result

