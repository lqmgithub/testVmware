# -*- coding:utf-8 -*-
from oslo_vmware import api
from oslo_vmware import vim_util

# Get a handle to a vSphere API session
session = api.VMwareAPISession(
    '192.168.103.110',      # vSphere host endpoint
    'root', # vSphere username
    'root123',      # vSphere password
    10,              # Number of retries for connection failures in tasks
    0.1              # Poll interval for async tasks (in seconds)
)

# Example call to get all the managed objects of type "HostSystem"
# on the server.
# result = session.invoke_api(
#     vim_util,                           # Handle to VIM utility module
#     'get_objects',                      # API method name to invoke HostSystem
#     session.vim, 'VirtualMachine',1, ["config"],all_properties=False)     # Params to API method (*args)



def _get_token(results):
    """Get the token from the property results."""
    return getattr(results, 'token', None)

vmlist = []
def buildList(result):
    for obj in result.objects:
        if not hasattr(obj, 'propSet'):
            continue
        property_dict = {}
        property_dict[obj.obj._type]=obj.obj.value
        dynamic_properties = obj.propSet
        if dynamic_properties:
            for prop in dynamic_properties:
                property_dict[prop.name] = prop.val
        return property_dict;
 


result = session.invoke_api(vim_util, "get_objects", session.vim,
                                  #"VirtualMachine",1, ['guest','summary','config.hardware.numCoresPerSocket','config.hardware.numCPU','config.hardware.memoryMB'])
                                  "VirtualMachine",1, ['name','config.hardware.numCoresPerSocket','config.hardware.numCPU','config.hardware.memoryMB'],)


while result:
   print result
   vmjson = buildList(result)
   vmlist.append(vmjson)
   result = session.invoke_api(vim_util, "continue_retrieval", session.vim,result)
session.logout();
print vmlist[1]

print "done"
#buildList(result2)
#print str(vmlist).decode('utf-8').encode('utf-8')


