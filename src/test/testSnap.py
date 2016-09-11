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


client_factory = session.vim.client.factory
managedObjectReference = client_factory.create('ns0:ManagedObjectReference')
managedObjectReference._type = "VirtualMachineSnapshot"
managedObjectReference.value = "39-snapshot-1"

reset_task = session.invoke_api(session.vim,"CreateSnapshot_Task", managedObjectReference,name="testnsap",description="ddd",memory=False,quiesce=False)
print reset_task

#reset_task = session.invoke_api(session.vim,"RemoveSnapshot_Task", managedObjectReference,removeChildren=False)
#print reset_task

# reset_task = session.invoke_api(session.vim,"RevertToSnapshot_Task", managedObjectReference)
# print reset_task

#session.invoke_api(session.vim,"RenameSnapshot", managedObjectReference,name="hahah")



session.wait_for_task(reset_task);
print "done"