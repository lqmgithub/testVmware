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


result = session.invoke_api(vim_util, "get_objects", session.vim,
                                  "VirtualMachine",10, ['config.extraConfig["RemoteDisplay.vnc.port"]'])
print result
vnc_ports = set()
while result:
    for obj in result.objects:
        if not hasattr(obj, 'propSet'):
            continue
        dynamic_prop = obj.propSet[0]
        option_value = dynamic_prop.val
        vnc_port = option_value.value
        vnc_ports.add(int(vnc_port))
    token = _get_token(result)
    if token:
        result = session.invoke_api(vim_util,
                                      "continue_to_get_objects",
                                      token)
    else:
        break
print  vnc_ports



