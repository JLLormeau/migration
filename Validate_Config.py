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
import sys

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
Name_TENANT={GCPTenant : ENV+'_GCP', AWSTenant: ENV+'_AWS', AZRTenant : ENV+'_AZR', INTRATenant: ENV+'_INTRA'}

##################################
### Environment saas
##################################
SaasTenant="https://"+str(os.getenv('SaasTenant'))
SaasToken=os.getenv('SaasToken')

##################################
## Variables
##################################

Mapping ={'ALERTING-PROFILE' : '/api/config/v1/alertingProfiles', \
          'ANOMALY-DETECTION-METRICS' : '/api/config/v1/anomalyDetection/metricEvents', \
          'APP-DETECTION-RULE-V2' : '/api/config/v1/applicationDetectionRules', \
          'APPLICATION-MOBILE' : '/api/config/v1/applications/mobile', \
          'APPLICATION-WEB' : '/api/config/v1/applications/web', \
          'AUTO-TAG' : '/api/config/v1/autoTags' , \
          'AWS-CREDENTIALS' : '/api/config/v1/aws/credentials', \
          'AZURE-CREDENTIALS' : '/api/config/v1/azure/credentials', \
          'CALCULATED-METRICS-APPLICATION-WEB' :  '/api/config/v1/calculatedMetrics/rum' , \
          'CALCULATED-METRICS-SERVICE' : '/api/config/v1/calculatedMetrics/service' , \
          'CREDENTIAL-VAULT' : '/api/config/v1/credentials' , \
          'CUSTOM-SERVICE-PHP' : '/api/config/v1/service/customServices/php', \
          'CUSTOM-SERVICE-NODEJS' : '/api/config/v1/service/customServices/nodeJS', \
          'CUSTOM-SERVICE-JAVA' : '/api/config/v1/service/customServices/java', \
          'DASHBOARD-V2' : '/api/config/v1/dashboards' ,  \
          'EXTENSION' : '/api/config/v1/extensions' ,  \
          'EXTENSION-V2' : '/api/v2/extensions', \
          'MAINTENANCE-WINDOW' : '/api/config/v1/maintenanceWindows', \
          'MANAGEMENT-ZONE':'/api/config/v1/managementZones', \
          'NOTIFICATION' : '/api/config/v1/notifications', \
          'REQUEST-ATTRIBUTES' : '/api/config/v1/service/requestAttributes' , \
          'SLO' : '/api/v2/slo', \
          'SYNTH_LOCATION': '/api/v1/synthetic/locations', \
          'SYNTHETIC-MONITOR': '/api/v1/synthetic/monitors'
          }

#defaut DataStore = 'values'		  
DataStore={'SLO': 'slo', \
           'SYNTHETIC-MONITOR': 'monitors', \
           'SYNTH_LOCATION' : 'locations' , \
           'DASHBOARD-V2' : 'dashboards', \
           'MAINTENANCE-WINDOW' : 'values' , \
           'AWS-CREDENTIALS' : '', \
           'CREDENTIAL-VAULT' : 'credentials' ,\
           'EXTENSION': 'extensions' ,\
           'EXTENSION-V2' : 'extensions'
           }


#defaut MappingID = 'id'
MappingID={ 'SYNTHETIC-MONITOR': 'entityId', \
            'SYNTH_LOCATION' : 'entityId' ,\
            'EXTENSION-V2': 'extensionextensionName' }

#defaut MappingName = 'name'
MappingName={'EXTENSION-V2': 'extensionName' }

#Default 
Parameter={ 'SLO' : '?pageSize=10000&sort=name&timeFrame=CURRENT&demo=false&evaluate=false&enabledSlos=true&showGlobalSlos=true&Api-Token='}

    

#disable warning
urllib3.disable_warnings()

# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
head = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}

Listapi=[]
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


   
##################################
## list of API
##################################
def info_api_managed(TENANT,TOKEN,API):

    #defaut DataStore = 'values'
    if API not in DataStore :
        DataStore[API] = 'values'

    #defaut MappingID = 'id'
    if API not in MappingID :
        MappingID[API] = 'id'

    #defaut MappingName = 'name'
    if API not in MappingName :
        MappingName[API] = 'name'
        
    #defaut Parameter = '?Api-Token='
    if API not in Parameter :
        Parameter[API] = '?Api-Token='


    uri=TENANT+Mapping[API]+Parameter[API]+TOKEN
  
    #print(uri)
    #print(DataStore[API])
    i=1
    j=1
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    if datastore != []:
        if DataStore[API] != '': 
            apilist = datastore[DataStore[API]]
            for entity in apilist:
                #print(entity)
                if entity[MappingName[API]] not in RESULT_MANAGED:
                    #print(entity[MappingName[API]])
                    RESULT_MANAGED.append(entity[MappingName[API]])
                    j+=1
                i+=1
        else:
            apilist = datastore
            for entity in apilist:
                #print(entity)
                if entity[MappingName[API]] not in RESULT_MANAGED:
                    #print(entity[MappingName[API]])
                    RESULT_MANAGED.append(entity[MappingName[API]])
                    j+=1
                i+=1
            
    print(API, Name_TENANT[TENANT], i-1, j-1)
        
        
    return ()

##################################
## list of API
##################################
def info_local_rep(TENANT,TOKEN,API):
    uri=TENANT+Mapping[API]+'?Api-Token='+TOKEN
    
    #print(uri)
    #print(DataStore[API])
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    if datastore != []:
        if DataStore[API] != '': 
            apilist = datastore[DataStore[API]]
            for entity in apilist:
                if entity[MappingName[API]] not in RESULT_SAAS:
                    RESULT_SAAS.append(entity[MappingName[API]])
        else:
            apilist = datastore
            for entity in apilist:
                if entity[MappingName[API]] not in RESULT_SAAS:
                    RESULT_SAAS.append(entity[MappingName[API]])
            
    return ()




##################################
## Main program
##################################
if len(sys.argv) > 1 :
    del(sys.argv[0])
    for i in sys.argv :
        Listapi.append(i)
else:
    for i in Mapping:
        Listapi.append(i)

for api  in Listapi:
    RESULT_MANAGED=[]
    RESULT_SAAS=[]

    print()
    print(api)

    #collect managed
    for tenant in Managed_TENANT:
        info_api_managed(tenant, Managed_TENANT[tenant], api)
    
    print(api, "Managed Tenants",  len(RESULT_MANAGED))
 
    #collect saas
    info_local_rep(SaasTenant, SaasToken, api)
    print(api, "Saas Tenant", len(RESULT_SAAS))

    #mapping
    for i in RESULT_MANAGED:
        if i not in RESULT_SAAS :
            print(i)

    #print(RESULT_SAAS)

print("###")
