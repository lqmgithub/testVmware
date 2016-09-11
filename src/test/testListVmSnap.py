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
 
 
 
def buildSnapshot(snapshotList,currentSnapshotVal):
    snapVoList = [];
    for snapvo in snapshotList:
        property_dict = {}
        property_dict["snapId"] = snapvo.snapshot.value;
        property_dict["vmId"] = snapvo.vm.value;
        property_dict["name"] = snapvo.name;
        property_dict["description"] = snapvo.description;
        property_dict["createTime"] = snapvo.createTime;
        property_dict["state"] = snapvo.state;
        property_dict["quiesced"] = snapvo.quiesced;
        property_dict["replaySupported"] = snapvo.replaySupported;
        property_dict["description"] = snapvo.description;
        property_dict["currentSnapshot"] = False
        if currentSnapshotVal and currentSnapshotVal == property_dict["snapId"]:
            property_dict["currentSnapshot"] = True
        snapVoList.append(property_dict);
        if  hasattr(snapvo, 'childSnapshotList'):
            snapVoList = snapVoList  + buildSnapshot(snapvo.childSnapshotList,currentSnapshotVal);
    return snapVoList;
 
 
 
 
 
vmsnapList = []
def buildList(result):
    for obj in result.objects:
        if not hasattr(obj, 'propSet'):
            continue
       
        dynamic_properties = obj.propSet
        if dynamic_properties:
            for prop in dynamic_properties:
                if prop.name == "snapshot" :
                    snapshotInfo = prop.val
                    snapshotList = snapshotInfo.rootSnapshotList
                    return buildSnapshot(snapshotList,snapshotInfo.currentSnapshot.value)
               
        return [];

result = session.invoke_api(vim_util, "continue_retrieval", session.vim,result)
print buildList(result)
session.logout();
print "done"


#buildList(result2)
#print str(vmlist).decode('utf-8').encode('utf-8')


