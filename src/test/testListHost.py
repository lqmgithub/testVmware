from oslo_vmware import api
from oslo_vmware import vim_util

# Get a handle to a vSphere API session
session = api.VMwareAPISession(
    '192.168.103.200',      # vSphere host endpoint
    'administrator@vsphere.local', # vSphere username
    '!@#4qwerFDSA',      # vSphere password
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
                                  "VirtualMachine",10)
  

print result;