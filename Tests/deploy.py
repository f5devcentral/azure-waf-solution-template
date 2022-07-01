import time, os, sys
path= "/home/runner/work/azure-waf-solution-template-/azure-waf-solution-template-"
sys.path.insert(0, path)
from Lib.utils import *
from Lib.var import *
from art import *

#Get the service principal and secret values
principal= sys.argv[1]
password = sys.argv[2]

print(text2art("Azure CFT Deploy",font="small"))
print("Connecting to Azure CLI") 
 

az_id = az_login(principal,password,tenantid)
if az_id:
    try:
        """If login success, then deploy resources."""
        print("AZ Login Sucessfull!!")
        print(banner("Validating the user given params"))
        validate_user_params()      
        
        print('Deploying the Virtual Machine Scale Set')
        az_arm_deploy(resource_group,autoscale_template,autoscale_param,resource="cft")
        print("Add the required Rules to the Security Group\n HTTP:")
        az_get_cmd_op(http_rule)
        print("SSH:")
        az_get_cmd_op(ssh_rule)
        print("Deploy the Telemetry")
        az_arm_deploy(resource_group,template_db,template_dbparam,resource="db")
        print(banner("Deployment Completed"))
        
    except BaseException:
        logging.exception("An exception was thrown!")
else:
    print("Error: Unable to connect to Azure CLI")

