#JLL
import json
import requests
import calendar
import os
import urllib3
import time
import re
#from json import JSONEncoder
import csv

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
Env_Source=os.getenv('tenant')
if Env_Source == None:
    Env_Source='ALL'

##################################
### Environment saas
##################################
SaasTenant="https://"+str(os.getenv('SaasTenant'))
SaasToken=os.getenv('SaasToken')

##################################
## Variables
##################################
Mapping ={'MZ':'/api/config/v1/managementZones', 'APP_WEB' : '/api/config/v1/applications/web', 'APP_MOBILE' : '/api/config/v1/applications/mobile', 'RequestAttribute' : '/api/config/v1/service/requestAttributes' , 'SLO' : '/api/v2/slo', 'SYNTH': '/api/v1/synthetic/monitors' , 'SYNTH_LOCATION': '/api/v1/synthetic/locations' , 'Dashboards' : '/api/config/v1/dashboards' , 'AlertingProfile' : '/api/config/v1/alertingProfiles'}
DataStore={'MZ':'values', 'APP_WEB':'values', 'APP_MOBILE':'values', 'RequestAttribute': 'values', 'SLO': 'slo', 'SYNTH': 'monitors', 'SYNTH_LOCATION' : 'locations' , 'Dashboards' : 'dashboards', 'AlertingProfile' : 'values'}
MappingID={'MZ':'id', 'APP_WEB':'id', 'APP_MOBILE':'id', 'RequestAttribute': 'id', 'SLO': 'id', 'SYNTH': 'entityId', 'SYNTH_LOCATION' : 'entityId' , 'Dashboards' : 'id' , 'AlertingProfile' : 'id'}
#Mapping ={'Dashboards' : '/api/config/v1/dashboards' }


# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
DIRECTORY = "./"+ENV+"_"MAPP/"
if os.name == 'nt':
    DIRECTORY = ".\\"+ENV+"_MAPP\\"

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

   
##################################
## list of API
##################################
def info_api(TENANT,TOKEN,API):
    uri=TENANT+Mapping[API]+'?Api-Token='+TOKEN
    RESULT={}

    #print(uri)
    #print(DataStore[API])
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    if datastore != []:
        apilist = datastore[DataStore[API]]
        for entity in apilist:
            RESULT[entity[MappingID[API]]]=entity['name']
        
        
    return (RESULT)

##################################
## Mapping
##################################
def mapping(DIC_MANAGED,DIC_SAAS):
    
    for id_managed in DIC_MANAGED:
            mapping=False
            for id_saas in DIC_SAAS:
                if DIC_SAAS[id_saas] == DIC_MANAGED[id_managed]:
                    if id_saas != id_managed:
                        MAPP[id_managed]=id_saas+";"+DIC_SAAS[id_saas]+";"+DIC_MANAGED[id_managed]
                    mapping=True
            if not(mapping):
                MISSING[DIC_MANAGED[id_managed]]=id_managed
                
    return (MAPP)


##################################
## Main program
##################################
if not(os.path.exists(DIRECTORY)):
    os.makedirs(DIRECTORY)


for api  in Mapping:
    DIC_RESULT_MANAGED={}
    DIC_RESULT_SAAS={}
    MAPP={}
    MISSING={}
    print(api, Mapping[api])
    file_test=False

    #test cache
    if os.path.exists(DIRECTORY+api+'_id_source.csv'):
        if os.path.getsize(DIRECTORY+api+'_id_source.csv') != 0:
            print('use local cache '+DIRECTORY+api+'_id_source.csv')
            file_test=True
            f= open(DIRECTORY+api+'_id_source.csv',encoding='utf-8')
            f = csv.reader(f,delimiter = ';')
            for row in f:
                if row != []:
                    DIC_RESULT_MANAGED[row[0]]=row[1]

    #collect managed
    if not(file_test):
        for tenant  in Managed_TENANT:
            DIC_RESULT_MANAGED.update(info_api(tenant, Managed_TENANT[tenant], api))
            fichier = open(DIRECTORY+api+'_id_source.csv', "w", encoding="utf-8")
            for id in DIC_RESULT_MANAGED :
                fichier.write(id+";"+DIC_RESULT_MANAGED[id]+"\n")
            fichier.close()
			
    #print(api, tenant, len(DIC_RESULT_MANAGED))
            print(api, "Managed Tenants",  len(DIC_RESULT_MANAGED))
 
    #collect saas
    DIC_RESULT_SAAS=info_api(SaasTenant, SaasToken, api)
    print(api, "Saas Tenant", len(DIC_RESULT_SAAS))

    #mapping
    mapping(DIC_RESULT_MANAGED,DIC_RESULT_SAAS)
    print(api, "mapping", len(MAPP))
    print(api, "missing", len(MISSING))
	
    #generate file
    fichier = open(DIRECTORY+api+'_mapping.csv', "w", encoding="utf-8")
    for id in MAPP :
        fichier.write(id+";"+MAPP[id]+"\n")
    fichier.close()

    fichier = open(DIRECTORY+api+'_missing.csv', "w", encoding="utf-8")
    for id in MISSING :
	    fichier.write(id+";"+MISSING[id]+"\n")
    fichier.close()

print("end")
