# -*- coding:utf-8 -*-
from oslo_vmware import api
from oslo_vmware import vim_util

# Get a handle to a vSphere API session
session = api.VMwareAPISession(
    '192.168.103.201',      # vSphere host endpoint
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






result = session.invoke_api(vim_util, "get_objects", session.vim,
                                  #"VirtualMachine",1, ['guest','summary','config.hardware.numCoresPerSocket','config.hardware.numCPU','config.hardware.memoryMB'])
                                  "VirtualMachine",1,None,True)
while result:
   print result
   print "******************************"
# vmlist = [];
# 
# def buildList(result):
#     for obj in result.objects:
#         if not hasattr(obj, 'propSet'):
#             continue
#         property_dict = {}
#         property_dict[obj.obj._type]=obj.obj.value
#         dynamic_properties = obj.propSet
#         if dynamic_properties:
#             for prop in dynamic_properties:
#                 property_dict[prop.name] = prop.val
#                 if prop.name == 'guest':
#                     print prop.val.guestState;
#         dynamic_prop = obj.propSet[0]
#         option_value = dynamic_prop.val
#         vmlist.append(property_dict);
# 
# buildList(result)

   result = session.invoke_api(vim_util, "continue_retrieval", session.vim,result)
session.logout();
print "done"


#buildList(result2)
#print str(vmlist).decode('utf-8').encode('utf-8')


