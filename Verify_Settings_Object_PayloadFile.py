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
import math
import time
import argparse

##################################
### Environment cible
##################################
SaasTenant="https://"+str(os.getenv('SaasTenant'))
SaasToken=os.getenv('SaasToken')

TestTenant="https://"+str(os.getenv('TestTenant'))
TestToken=os.getenv('TestToken')

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
# loading bar
#================================================
def progressbar(it, prefix="", size=60, out=sys.stdout,): # Python3.3+
    count = len(it)
    def show(j):
        x = int(size*j/count)
        print("{}[{}{}] {}/{}".format(prefix, "█"*x, "."*(size-x), j, count), 
                end='\r', file=out, flush=True)
    show(0)
    for i, item in enumerate(it):
        yield item
        show(i+1)
    print("\n", flush=True, file=out)
    
#================================================
# Functions
#================================================

def post_payload_from_objects():
    
     url = SaasTenant +"/api/v2/settings/objects?validateOnly=true&Api-Token="+ SaasToken
     #print(url)
     list2 = []
     file = open(sys.argv[1])
     list = json.load(file)
     total=len(list)
     
     
     for i in progressbar(range(total), "Verification: ", 70,):
        result = postDynatraceAPI(url, list[i])
        list2.append(result)
    
        
     
     print(*list2, sep = "\n")



            
     return()


  
##################################
## Main program
##################################

post_payload_from_objects()




    


    
    



