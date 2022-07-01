import time, os, sys
path= "/home/runner/work/azure-waf-solution-template-/azure-waf-solution-template-"
sys.path.insert(0, path)
from Lib.utils import *
from Lib.var import *
from Lib.attackslib import *
from art import *

#Get the service principal and secret values
principal= sys.argv[1]
password = sys.argv[2]

print("Connecting to Azure CLI")
az_id = az_login(principal,password,tenantid)
if az_id:
    try:  
        print(text2art("CFT Destroy",font="small"))
        print(banner("Destroying the Infra."))
        for service in del_cfg:
            print(service)
            az_get_cmd_op(service) 
            time.sleep(7)
        print(banner("Infra destroyed sucessfully!!!"))
    except BaseException:
        logging.exception("An exception was thrown under Destroy!")
else:
    print("Error: Unable to connect to Azure CLI")
