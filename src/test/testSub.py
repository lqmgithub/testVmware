from suds.client import Client
url = 'https://192.168.103.200/sdk/vimService.wsdl'
client = Client(url) 
print client