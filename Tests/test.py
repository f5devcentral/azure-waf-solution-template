import time, os, sys, json, ast
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
        
        print(text2art("CFT Testcase Execution",font="small"))
        #Get the instance details from Virtual machine scaleset
        print(banner("+"))
        print(banner("TC-0 Infra Validation"))
        print(banner("+"))
        print("Get VMSS Instance details")
        inst_info=az_get_cmd_op(get_vmss)
        vmss_ip_lst=get_ip(inst_info)
        vmss_port_list=get_port_lst(inst_info)  
        print("Get Telemetry Details")       
        dashboard_info=az_get_cmd_op(db_verify)
        
        if NAP_TEST:
            try:
                #NAP Functional Test
                turn_instance_state(str(vmss_port_list[1])[-1],"stop",vmssName,resource_group)
                print(banner("+"))
                print(banner("TC-1: NAP Static Page Verification"))
                print(banner("+"))
                if vfy_nginx(vmss_ip_lst[0],chk_def):
                    print("*** NGINX Static Page Verification is Completed!!! *** \n")
                else:
                    print("ERROR:  NGINX Static Page Verification is Failed!!!")
                
                print(banner("+"))                
                print(banner("TC-2: NAP Dynamic Page Verification"))
                print(banner("+"))
                ssh_id=ssh_connect(vmss_ip_lst[0],vmss_port_list[0],username,vm_password)
                if ssh_id != "retry":
                    with SCPClient(ssh_id.get_transport()) as scp:  scp.put('Lib/nginx_conf_nap.conf','nginx.conf')
                    for cmd in [command_lst,command_lst2]:
                        exec_shell_cmd(ssh_id,cmd)
                        time.sleep(10)
                
                if vfy_nginx(vmss_ip_lst[0],chk_str):
                    print("*** Nginx App Protect dynamic page verification with Arcadia Application is Successfull!!! *** \n")
                    print(banner("+"))
                    print(banner("TC-3: NAP Testing with malicious attacks"))
                    print(banner("+"))                
                    print("\n***      cross script      ***")
                    output = cross_script_attack(vmss_ip_lst[0])
                    print(output)
                    assert "support ID" in output
                    print("***      cross script attack blocked. ***")
                    print("\n***      sql injection       ***")
                    output = sql_injection_attack(vmss_ip_lst[0])
                    print(output)
                    assert "support ID" in output
                    print("***   sql injection script attack blocked.  ***")
                    print("\n***      command injection       ***")
                    output = command_injection_attack(vmss_ip_lst[0])
                    print(output)
                    assert "support ID" in output
                    print("***      command injection attack blocked. ***")
                    print("\n***      directory traversal      ***")
                    output = directory_traversal_attack(vmss_ip_lst[0])
                    print(output)
                    assert "support ID" in output
                    print("***    directory traversal attack blocked.    ***")
                    print("\n***      file inclusion      ***")
                    output = file_inclusion_attack(vmss_ip_lst[0])
                    print(output)
                    assert "support ID" in output
                    print("***   file inclusion attack blocked.   ***\n")
                else:
                    print(banner("ERROR: Nginx App Protect dynamic page verification is Failed!!!"))
                turn_instance_state(str(vmss_port_list[1])[-1],"start",vmssName,resource_group)
            except AssertionError:
                print("Encountered a Problem")
                raise
                
        if LB_TEST:
            print(banner("+"))
            print(banner("TC-4: Load Balancer TEST with Fault Tolarance"))
            print(banner("+"))
            turn_instance_state(str(vmss_port_list[1])[-2],"stop",vmssName,resource_group)
            time.sleep(30)

            if vfy_nginx(vmss_ip_lst[0],chk_def):
                print(banner("\t*** Load Balancer TEST with Fault Tolarance is Successfull ***\n"))
            else:
                print(banner("\t*** Load Balancer TEST with Fault Tolarance is Failed!!! ***\n"))
            turn_instance_state(str(vmss_port_list[1])[-2],"restart",vmssName,resource_group)
        
        if AutoScale_TEST:
            try:
                print("\n Make sure both the instances are UP")
                turn_instance_state(str(vmss_port_list[1])[-2],"start",vmssName,resource_group)
                time.sleep(60)
                print(banner("+"))
                print(banner("TC-5: AutoScale TEST "))
                print(banner("+"))
                print("Current No of instances under VMSS:",vmssName,vmss_ip_lst,vmss_port_list)
                print("Imposing HIGH TRAFFIC on available instances")
                vmss_port_list.reverse()
                for port in vmss_port_list:
                    print("Connecting to ",vmss_ip_lst[0],":",port)
                    ssh_id=ssh_connect(vmss_ip_lst[0],port,username,vm_password)
                    if ssh_id != "retry": exec_shell_cmd(ssh_id,apply_stress)

                print("Minimum of amount of traffic duration to trigger the auto-scaling action: 5 Minutes")
                time.sleep(500)
                print("Number of Instances after Imposing high traffic")                
                inst_info= az_get_cmd_op(get_vmss)
                vmss_ip_lst=get_ip(inst_info) 
                if len(get_port_lst(inst_info)) > 2:
                    print("*** Auto-Scale Test is Completed Successfully!!! ***")
                else:
                    print("Error: Scaling Test is Failed!!!")
                for port in vmss_port_list:
                    ssh_id=ssh_connect(vmss_ip_lst[0],port,username,vm_password)
                    if ssh_id != "retry": exec_shell_cmd(ssh_id,remove_stress)
            except SSHException as sshException:
                print(banner("Unable to establish SSH connection: %s" % sshException))
else:
    print("Error: Unable to connect to Azure CLI")
