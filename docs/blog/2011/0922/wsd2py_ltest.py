# import the generated class stubs
import countries_webservice_mobilefish_com_client as client
import countries_webservice_mobilefish_com_server as server
# get a port proxy instance
loc = client.countries_webservice_mobilefish_comServiceLocator()
#~ addr = loc.getcountries_webservice_mobilefish_comPortAddress()
port = loc.getcountries_webservice_mobilefish_comPort()
# create a new request
req = server.countryInfoByIanaRequest(ianacode='be')
#~ req.Options = req.new_Options()
#~ req.Options.Query = ’newton’
# call the remote method
resp = port.WolframSearch(req)
# print results
print ’Search Time:’, resp.Result.SearchTime
print ’Total Matches:’, resp.Result.TotalMatches
for hit in resp.Result.Matches.Item:
print ’--’, hit.Title