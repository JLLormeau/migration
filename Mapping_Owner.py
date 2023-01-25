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
ENV='DEV'

Cluster=os.getenv('Cluster')
ClusterToken=os.getenv('ClusterToken')
Cookie=os.getenv('Cookie')
CSRFToken=os.getenv('CSRFToken')


##################################
## Variables
##################################
Mapping = {}
API_GET_USERS="/api/v1.0/onpremise/users"
USER_GROUPS = "/api/v1.0/onpremise/groups"


# variable changed if script is run on Windows or Linux. "\\" for Windows, "/" for Linux
DIRECTORY = "./"+ENV+"_MAPP/"
if os.name == 'nt':
    DIRECTORY = ".\\"+ENV+"_MAPP\\"

#disable warning
urllib3.disable_warnings()

head = {
    'Accept': 'application/json',
    'Content-Type': 'application/json; charset=UTF-8'
}
RESULT={}


head = {
    'Authorization': 'Api-Token {}'.format(ClusterToken),
	'X-CSRFToken': CSRFToken,
	'Cookie': Cookie
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


   
##################################
## list of API
##################################
def info_api(TENANT,TOKEN,API):
    #uri=TENANT+API+'?Api-Token='+TOKEN
    uri=TENANT+API
    RESULT={}

    print(uri+'?Api-Token='+TOKEN)
    listentityid=[]
    DoublonTodelete=[]
    datastore = queryDynatraceAPI(uri)
    #print(datastore)
    if datastore != []:
        for apilist in datastore :
            RESULT[apilist['id']]=apilist['email']
        
    return (RESULT)


##################################
## Main program
##################################
if not(os.path.exists(DIRECTORY)):
    os.makedirs(DIRECTORY)


RESULT=info_api(Cluster, ClusterToken, API_GET_USERS)
fichier = open(DIRECTORY+'owner_mapping.csv', "w")
i=0
for user in RESULT:
    print(user+";"+RESULT[user]+";")
    fichier.write(user+";"+RESULT[user]+";\n")
    i+=1
fichier.close()


print("end")


    

