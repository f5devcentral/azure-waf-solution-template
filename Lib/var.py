import json,sys
path= "/home/runner/work/azure-waf-solution-template-/azure-waf-solution-template-"
sys.path.insert(0, path)

NAP_TEST = True
LB_TEST = True
AutoScale_TEST = True

#Variable Declaration
azure_user_json= "Lib/azure_user_params.json"
azure_user_handler = open(azure_user_json, "r")
azure_user_data = json.load(azure_user_handler)
tenantid = azure_user_data["tenandId"]
resource_group = azure_user_data["resourceGroup"]
username = azure_user_data["adminUsername"]
vm_password = azure_user_data["adminPassword"]
vnet_name= azure_user_data["virnetworkId"]
vmssName= azure_user_data["cftName"]
vmss_lb= azure_user_data["cftName"] + "-lb"
vmss_ip= azure_user_data["cftName"] + "-ip"
db_name= azure_user_data["dashboard_name"]
autoscale_template= "Templates/nap-autoscale-ubuntu-dev.json"
autoscale_param= "Templates/nap-autoscale-ubuntu-dev-params.json"
template_db= "Templates/dashboard.json"
template_dbparam = "Templates/dashboard-params.json"
sg_name= "basicNsg" + vnet_name + "-nic01"
http_rule= "az network nsg rule create -g " + resource_group + " --nsg-name " + sg_name + " --name httpRule --direction inbound --destination-port-range 80 --access allow --priority 102 --output table"
ssh_rule=  "az network nsg rule create -g " + resource_group + " --nsg-name " + sg_name + " --name sshRule --direction inbound --destination-port-range 22 --access allow --priority 101 --output table"
get_vmss= "az vmss list-instance-connection-info   --resource-group " + resource_group + " --name " + vmssName + " --output table"
chk_str="Arcadia Finance"
chk_def = "Welcome to NGINX Plus on Azure"
command_lst = ["ls", "sudo cp nginx.conf /etc/nginx/nginx.conf" , "sudo systemctl restart nginx"]
command_lst2 = ["systemctl status nginx"]
log_file= "./Log/vm_log.txt"
apply_stress= ["for i in $(seq $(getconf _NPROCESSORS_ONLN)); do yes > /dev/null & done"]
remove_stress=["killall yes"]
db_verify="az portal dashboard show --name " + db_name + " --resource-group " + resource_group + " --output table"
del_vmss= "az vmss delete  --name " + vmssName + " --resource-group " + resource_group + " --force-deletion yes"
del_vmss_lb= "az network lb delete --name " + vmss_lb + "  --resource-group " + resource_group
del_dashboard="az portal dashboard delete --name " + db_name + "  --resource-group " + resource_group + " -y "
del_vmss_ip= " az network public-ip delete -g " + resource_group + " -n " + vmss_ip
del_ssh= "az network nsg rule delete -g " + resource_group + " --nsg-name " + sg_name + " -n sshRule"
del_http= "az network nsg rule delete -g " + resource_group + " --nsg-name " + sg_name + " -n httpRule"
del_vnetId=  "az network vnet delete --name " + azure_user_data["virnetworkId"] + " -g " + azure_user_data["resourceGroup"]
del_wrkspace= "az monitor log-analytics workspace delete -g "  + azure_user_data["resourceGroup"] + " --workspace-name " + azure_user_data["workspaceName"] + " -y"
del_cfg=[del_vmss,del_ssh,del_http,del_vmss_lb,del_vmss_ip,del_dashboard,del_vnetId,del_wrkspace]
