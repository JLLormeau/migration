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

##Simu managed JLL
#Managed_TENANT={"https://"+str(os.getenv('ManagedDemo')): os.getenv('ManagedDemoToken')}

print('=> target : '+SaasTenant)

##################################
## Variables
##################################
period='now-3d'
Mapping = {}
API_ENTITY_TYPE='/api/v2/entityTypes'
LISTENTITY=[]
#LISTENTITY=['HOST_GROUP', 'APPLICATION']
#LISTENTITY=['CLOUD_APPLICATION_INSTANCE']

# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
DIRECTORY = "./"+ENV+"_"+Env_Source+"_MAPP/"
if os.name == 'nt':
    DIRECTORY = ".\\"+ENV+"_"+Env_Source+"_MAPP\\"

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
    uri=TENANT+Mapping[API]+'&Api-Token='+TOKEN
    #print(uri)
    RESULT={}

    #print(uri)
    listentityid=[]
    DoublonTodelete=[]
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    if datastore != []:
        apilist = datastore['entities']
        totalCount=datastore['totalCount']
        #print('apilist',len(apilist))
        if totalCount > 12000:
            nextPageKey=datastore['nextPageKey']
            print(' totalCount',totalCount)
            print('  #entities are loading in entity list',len(apilist))
            while nextPageKey != '' :
                datastore2={}
                uri=TENANT+'/api/v2/entities?nextPageKey='+nextPageKey+'&Api-Token='+TOKEN
                #print(uri)
                datastore2=queryDynatraceAPI(uri)
                totalCount=datastore2['totalCount']
                if 'nextPageKey' in datastore2:
                    nextPageKey=datastore2['nextPageKey']
                else:
                    nextPageKey =''
                apilist=apilist+datastore2['entities']
                print('  #entities are loading in entity list',len(apilist))
            print(' entities are mapping...')
        i=0
        j=0
        for entity in apilist:
            if entity['displayName'] not in listentityid :
                RESULT[entity['entityId']]=entity['displayName']
                listentityid.append(entity['displayName'])
                j+=1
            else :
                if entity['displayName'] not in DoublonTodelete:
                    DoublonTodelete.append(entity['displayName'])
                    i+=1
        print(' entities', j,'doublons', i)
    if DoublonTodelete != []:
        RESULT2=RESULT.copy()
        for row1 in DoublonTodelete :
            for row2 in RESULT.copy():
                if RESULT[row2]==row1:
                    del  RESULT[row2]
        RESULT=RESULT2
        
    return (RESULT)

##################################
## EntityTYpe
##################################
def generate_list_entitytype(TENANT, TOKEN):
    i=0
    uri=TENANT+API_ENTITY_TYPE+'?pageSize=400&Api-Token='+TOKEN
    #print(uri)
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    entityidlist = datastore['types']
    for entityid in entityidlist:
        #print(entityid['type'])
        if entityid['type'] not in Mapping and entityid['type']:
            Mapping[entityid['type']]='/api/v2/entities?'+period+'&pageSize=12000&entitySelector=type("'+entityid['type']+'")'
            print(i, entityid['type'])            
        
        i+=1
    #print(' #lines ='+str(i))
    return()

##################################
## Mapping
##################################
def mapping(DIC_MANAGED,DIC_SAAS):
    
    for id_managed in DIC_MANAGED:
            for id_saas in DIC_SAAS:
                if DIC_SAAS[id_saas] == DIC_MANAGED[id_managed]:
                    if id_managed != id_saas:
                        if id_saas not in DIC_MANAGED:
                            MAPP[id_managed]=id_saas+";"+DIC_SAAS[id_saas]+";"+DIC_MANAGED[id_managed]

                
    return (MAPP)


##################################
## Main program
##################################
if not(os.path.exists(DIRECTORY)):
    os.makedirs(DIRECTORY)


if LISTENTITY == []:
    for tenant  in Managed_TENANT:
        Mapping.update(generate_list_entitytype(tenant, Managed_TENANT[tenant]))
else:
    for entity in LISTENTITY:
        Mapping[entity]='/api/v2/entities?pageSize=12000&entitySelector=type("'+entity+'")'



print("#####################")
j=0

for api  in Mapping:
    DIC_RESULT_MANAGED={}
    DIC_RESULT_SAAS={}
    MAPP={}
    MISSING={}
    print(api, Mapping[api])
    file_test=False
    api_name=api.replace(":","_")

    #test cache
    if os.path.exists(DIRECTORY+'entity_'+api_name+'_id_source.csv'):
            print(j, api, 'use local cache '+DIRECTORY+'entity_'+api_name+'_id_source.csv')
            file_test=True
            f= open(DIRECTORY+'entity_'+api_name+'_id_source.csv',encoding='utf-8')
            f = csv.reader(f,delimiter = ';')
            for row in f:
                if row != []:
                    DIC_RESULT_MANAGED[row[0]]=row[1]

    #collect managed
    if not(file_test):
        for tenant  in Managed_TENANT:
            DIC_RESULT_MANAGED.update(info_api(tenant, Managed_TENANT[tenant], api))
            fichier = open(DIRECTORY+'entity_'+api_name+'_id_source.csv', "w",encoding='utf-8')
            for id in DIC_RESULT_MANAGED :
                fichier.write(id+";"+DIC_RESULT_MANAGED[id]+"\n")
            fichier.close()
			
    #print(api, tenant, len(DIC_RESULT_MANAGED))
    print(j, api, "Managed Tenants",  len(DIC_RESULT_MANAGED))
 
    #collect saas
    DIC_RESULT_SAAS=info_api(SaasTenant, SaasToken, api)
    #print(DIC_RESULT_SAAS)
    print(j, api, "Saas Tenant", len(DIC_RESULT_SAAS))

    #mapping
    mapping(DIC_RESULT_MANAGED,DIC_RESULT_SAAS)
    print(j, api, "mapping", len(MAPP))
	
    #generate file
    fichier = open(DIRECTORY+'entity_'+api_name+'_mapping.csv', "w",encoding='utf-8')
    for id in MAPP :
        fichier.write(id+";"+MAPP[id]+"\n")
    fichier.close()

    #fichier = open(DIRECTORY+'entity_'+api_name+'_missing.csv', "w")
    #for id in MISSING :
    #	    fichier.write(id+";"+MISSING[id]+"\n")
    #fichier.close()
    j+=1


print("end")


    

