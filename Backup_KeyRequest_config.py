#================================================
# Modules
#================================================
import requests
from urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(category=InsecureRequestWarning)
import ssl
import json
import argparse
import sys
import os
from configparser import ConfigParser
import urllib3

##################################
### Environment managed
##################################
ENV=os.getenv('env')
Cluster=os.getenv('Cluster')
ClusterToken=os.getenv('ClusterToken')
GCPTenant=Cluster+str(os.getenv('GCPTenant'))
GCPToken=os.getenv('GCPToken')
AWSTenant=Cluster+str(os.getenv('AWSTenant'))
AWSToken=os.getenv('AWSToken')
INTRATenant=Cluster+str(os.getenv('INTRATenant'))
INTRAToken=os.getenv('INTRAToken')
AZRTenant=Cluster+str(os.getenv('AZRTenant'))
AZRToken=os.getenv('AZRToken')

Managed_TENANT={GCPTenant: GCPToken, AWSTenant: AWSToken, AZRTenant: AZRToken, INTRATenant: INTRAToken}

##################################
### Environment saas
##################################
SaasTenant="https://"+str(os.getenv('SaasTenant'))
SaasToken=os.getenv('SaasToken')

##################################
### Paramètres schemaId
##################################

schemaIdgcp = ['settings.subscriptions.service']
schemaIdaws = ['settings.subscriptions.service']
schemaIdazr = ['settings.subscriptions.service']
schemaIdintra = ['settings.subscriptions.service']
##################################
### Other
##################################
#disable warning
urllib3.disable_warnings()

# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
head = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

##################################
## Generic Dynatrace API
##################################

# generic function GET to call API with a given uri
def queryDynatraceAPI(uri):
    jsonContent = None
    response = requests.get(uri,headers=head,verify=False)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)


#generic function POST to call API with a given uri
def postDynatraceAPI(uri, payload):
    jsonContent = None
    response = requests.post(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        if(len(response.text) > 0):
            jsonContent = json.loads(response.text)
            jsonContent="success"
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if(jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function PUT to call API with a given uri
def putDynatraceAPI(uri, payload):
    jsonContent = None
    #print(uri,head,payload)
    response = requests.put(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        jsonContent="success"
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if (jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#generic function Delete to call API with a given uri
def delDynatraceAPI(uri, payload):
    jsonContent = None
    #print(uri,head,payload)
    response = requests.delete(uri,headers=head,verify=False, json=payload)
    # For successful API call, response code will be 200 (OK)
    if(response.ok):
        jsonContent="success"
    else:
        jsonContent = json.loads(response.text)
        print(jsonContent)
        errorMessage = ""
        if (jsonContent["error"]):
            errorMessage = jsonContent["error"]["message"]
            print("Dynatrace API returned an error: " + errorMessage)
        jsonContent = None
        #raise Exception("Error", "Dynatrace API returned an error: " + errorMessage)

    return(jsonContent)

#================================================
# Functions
#================================================

def get_ID_from_objects(tenant, token, param,tenantName):
    url = tenant + param +"&Api-Token="+ token
    #print(url)
    datastore = queryDynatraceAPI(url)
    #print(datastore)
    items = datastore["items"]
    #print(items)
    listkeyrequest = []
    for item in items:
        dict = {}
        #print(item["objectId"])
        param = "/api/v2/settings/objects/"+ item["objectId"]
        url2 = tenant + param + "?Api-Token=" + token
        #print(url2)
        datastore = queryDynatraceAPI(url2)
        
        #print(datastore['summary'])
        
        dict.update([('schemaId', datastore['schemaId'])])
        #print(datastore['schemaId'])
        dict.update([('scope', datastore['scope'])])
        dict.update([('value', datastore['value'])])
        #print(dict)


        data =  [
            dict
            ]
        
        listkeyrequest.append(data)

    #1-Create file
    filename = "backup_keyRequest-" + ENV.lower() + "-" + tenantName + ".json" 
    print("Result in: " + filename)
    with open(filename, "w") as f:
        json.dump(listkeyrequest, f, indent=4) 
    f.close()
    return() 

    ##################################
## Main program
##################################
def main():
    print("From gcp")
    for i in schemaIdgcp:
     print(i)   
     param = "/api/v2/settings/objects?schemaIds=builtin%3Asettings.subscriptions.service&pageSize=500"
     tenant = GCPTenant
     token = GCPToken
     tenantName = "gcp"
     get_ID_from_objects(tenant, token, param,tenantName)

    print("From aws")
    for i in schemaIdaws:
     print(i)   
     param = "/api/v2/settings/objects?schemaIds=builtin%3Asettings.subscriptions.service&pageSize=500"
     tenant = AWSTenant
     token = AWSToken
     tenantName = "aws"
     get_ID_from_objects(tenant, token, param,tenantName)

    print("From azr")
    for i in schemaIdaws:
     print(i)   
     param = "/api/v2/settings/objects?schemaIds=builtin%3Asettings.subscriptions.service&pageSize=500"
     tenant = AZRTenant
     token = AZRToken
     tenantName = "azr"
     get_ID_from_objects(tenant, token, param,tenantName)

    print("From azr")
    for i in schemaIdaws:
     print(i)   
     param = "/api/v2/settings/objects?schemaIds=builtin%3Asettings.subscriptions.service&pageSize=500"
     tenant = INTRATenant
     token = INTRAToken
     tenantName = "intra"
     get_ID_from_objects(tenant, token, param,tenantName)
 



    


    
    

main()