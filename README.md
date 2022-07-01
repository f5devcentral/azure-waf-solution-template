# azure-waf-solution-template-

## Introduction:

In Production-grade deployment it is always a challenge for anyone who wants to give a demo in their environment with a WAF deployment.  Usually, it takes at least a few weeks for an average team to design and implement a production-grade WAF in a cloud environment because for each cloud deployment virtual networking, infrastructure security, Virtual Machine images, auto-scaling, logging, monitoring, automation, and many more topics requires detailed analysis. Also, most of well-made WAF deployments follow a similar path and become similar at the end. To mitigate this time and effort, we came up with a conclusion that a proper WAF deployment can be templatized and automated. So, a team doesn’t need to spend much time on deployment and maintenance but starts to use a WAF from day zero. 
In this article we introduced a project that implements a Cloud Formation templates to deploy production-grade WAF in Azure cloud just in a few clicks and few runs.The WAF is using NGINX App Protect official image which is available under AZURE marketplace that eliminates the need to manually prebuild the AMI for your WAF deployment. It contains all the necessary code and packages on top of the OS of your choice. Also, allows you to pay as you go for NGINX App Protect software instead of purchasing a year-long license. 


## Why Azure?

Globally, 90% of Fortune 500 companies are using Microsoft Azure to drive their business. Using deeply integrated Azure cloud services, enterprises can rapidly build, deploy, and manage simple to complex applications with ease. Azure supports a wide range of programming languages, frameworks, operating systems, databases, and devices, allowing enterprises to leverage tools and technologies they trust.
Here are the reasons received from the customers who are deploying their deployments in Azure.
•	Infrastructure as a Service (IaaS) and Platform as a Service (PaaS) capabilities
•	Security Offerings, Scalability and Ductility
•	Integrated Environment with Other Microsoft Tools
•	Cost Efficient and Interoperability

## Architecture:
![image](https://user-images.githubusercontent.com/39581520/174727809-8fde48cd-12eb-4d31-a428-1f7e83953418.png)


### Major components:

•	Auto-scaling data plane based on official NGINX App Protect AWS AMI images.
o	The amount of incoming traffic and the configured rule sets by using the official NGINX App Protect AZURE AMIs to spin up new Virtual Machine instances. It also removes the operational headache and optimizes costs since WAF dynamically adjusts the amount of computing resources and charges a user on an as-you-go basis.
•	ARM template spec/git repository with the source of data plane and security configuration.
o	Solution configuration follows Gitlab principles. The Pipeline runs the ARM templates which will connect to the azure portal and deploys the solution. Also, user can directly login to the Azure portal and can run the template under Template Spec which will deploy the solution directly.

•	Visibility dashboards displaying the WAF health and security data.
o	The template sets up a set of visibility dashboards in Azure Dashboard Service. Data plane VMs send logs and metrics to Dashboard service that visualizes incoming data as a set of charts and graphs showing WAF health and security violations.
Therefore, these three components form a complete WAF solution that is easy to deploy, doesn’t impose any operational headache and provides handy interfaces for WAF configuration and visibility right out of the box.

![image](https://user-images.githubusercontent.com/39581520/174728235-9e974956-6be9-4377-8bed-30990ec1ffff.png)

## Dashboard:

![image](https://user-images.githubusercontent.com/39581520/174728292-7c9aa06a-377d-4a35-94d2-11d6863a25a5.png)


## How to Run:

* Pre-requisites:
  * you should have the admin privillages to your azure resource group.
  * Login to azure portal (portal.azure.com)
  * Create the service principle through Az Cli. (how to create the service principle (https://docs.microsoft.com/en-us/cli/azure/create-an-azure-service-principal-azure-cli))
* Add the below variables under github-->secrets
   * AZURE_SP --> Azure service principle
   * AZURE_PWD --> Azure client password
   * RUNNER_PATH --> github runner path
* Add your resource group and other params under Lib/azure-user-params file.
* On GitHub.com, navigate to the main page of the repository.
* Under your repository name, click Actions.
* In the left sidebar, click the workflow you want to run.
* Above the list of workflow runs, select Run workflow.
* Use the Branch dropdown to select the workflow's branch, and type the input parameters.

## Conclusion:

Therefore, the use of a template to deploy a cloud WAF allows to significantly reduce time spent on WAF deployment and maintenance. Also, it gives a complete and easy-to-use solution to deploy the resources and verify the NGINX solution in Azure platform in any location. Handy interfaces for configuration and visibility turn this project into a boxed solution allowing a user to easily operate a WAF and focus on application security.
Please comment if you find useful to have this kind of solution in major public clouds marketplaces.
It is a community project so far, and we need as much feedback as possible to steer one properly. Feel free to give it a try and leave feedback here or at the project's git repository.

