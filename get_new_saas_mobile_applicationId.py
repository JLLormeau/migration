import sys
import json
from f_http import *
import getopt

#================================================
# Variables
#================================================

### Environment managed
ENV=os.getenv('env') #ENV = DEV | RE7 | OPE
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

### Environment saas
SaasTenant="https://"+str(os.getenv('SaasTenant'))
SaasToken=os.getenv('SaasToken')

### Mapping
Api ={'APP_MOBILE' : '/api/config/v1/applications/mobile'}
schemaIds={}

#================================================
# Functions
#================================================
def get(url, token, api):
    url = url + api
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_entity(url, token, api, entityId):
    url = url + api + "/" + entityId  #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId
    #print(url)
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

#================================================
# Main
#================================================

def main():

    #Get arguments
    try: 
        optlist, args = getopt.getopt(sys.argv[1:], 'x', [''])
        #print ('Argument list:') 
        #print(optlist) 
        #print(args)

    except getopt.GetoptError as err: # print help information and exit:
        print(err)  # will print something like "option -a not recognized"

    #Parse arguments
    '''for arg, value in optlist:
        if arg == '--tenant':
            tenant = optlist[0][1]'''
    
    print(SaasTenant)

    error, mobile_apps_saas = get(SaasTenant, SaasToken, Api["APP_MOBILE"])
    if error:
        print("Error - Get  mobile apps (SaaS)")
    else:
            manual_apps_saas_json = json.loads(mobile_apps_saas)

    appsIds=[]
    appsSia=[]
    cpt_saas = 0

    for app in manual_apps_saas_json["values"]: 
        appsIds.append(app["id"])

    #Pour toutes les applications mobiles (SaaS)
    for id in appsIds: 
        error, mobile_app_saas = get_entity(SaasTenant, SaasToken, Api["APP_MOBILE"], id)
        if error:
            print("Error - Get  mobile app (SaaS)")
        else:
            mobile_app_saas_json = json.loads(mobile_app_saas)
            if mobile_app_saas_json["applicationType"] == "MOBILE_APPLICATION":
                print(mobile_app_saas_json["name"]+"("+mobile_app_saas_json["identifier"] + "): " + mobile_app_saas_json["applicationId"])
                appsSia.append()
                cpt_saas+= 1

    print("SaaS applications: " + str(cpt_saas))
            
if __name__ == '__main__':
    main()

#__END__
