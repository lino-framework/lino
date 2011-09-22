"""
USAGE:

  python inspect_wsdl.py <URL>

Where <URL> must return the WSDL of a web service. Examples:
  
  http://www.mobilefish.com/services/web_service/countries.php?wsdl  

Thanks to http://diveintopython.org/soap_web_services/"""
import sys
from SOAPpy import WSDL

def inspect(wsdl_url):
    print wsdl_url
    proxy = WSDL.Proxy(wsdl_url)
    #~ proxy.soapproxy.config.dumpSOAPOut = 1
    #~ proxy.soapproxy.config.dumpSOAPIn = 1
    for k,v in proxy.methods.items():
        print '%s(%s)' % (k,','.join([(p.type[1]+' '+p.name) for p in v.inparams]))
        print '  --> ' + ','.join([(p.type[1]+' '+p.name) for p in v.outparams])
    print proxy.countryInfoByIana('be')

if __name__ == '__main__':
    if len(sys.argv) <= 1:
          print __doc__
          sys.exit(-1)
    for url in sys.argv[1:]:
        inspect(url)