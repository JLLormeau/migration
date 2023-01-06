import sys
import json
from f_http import *
import getopt
import time
import datetime

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
Api ={'APP_WEB' : '/api/config/v1/applications/web', 'APP_MOBILE' : '/api/config/v1/applications/mobile', 'KEY_USER_ACTION' : '/keyUserActions', 'ERROR_RULES' : '/errorRules', 'SETTINGS_OBJECT' : '/api/v2/settings/objects'}
schemaIds={'DATA_PRIVACY_SETTINGS_WEB':'builtin:preferences.privacy'}


#================================================
# Functions
#================================================
def get(url, token, api):
    url = url + api
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_entity(url, token, api, entityId, option):
    url = url + api + "/" + entityId + option #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId + "/keyUserActions"
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_settings_object(url, token, api, schemaIds, scopes, fields):
    schemaIds =  schemaIds.replace(":", "%3A")
    schemaIds =  schemaIds.replace(",", "%2C")
    url = url + api + "?schemaIds=" + schemaIds + "&scopes=" + scopes + "&fields=" + fields
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

#================================================
# Main
#================================================

def main():

    #Get arguments
    try: 
        optlist, args = getopt.getopt(sys.argv[1:], 'x', ['tenant='])
        #print ('Argument list:') 
        #print(optlist) 
        #print(args)

    except getopt.GetoptError as err: # print help information and exit:
        print(err)  # will print something like "option -a not recognized"

    #Parse arguments
    for arg, value in optlist:
        if arg == '--tenant':
            tenant = optlist[0][1] 

    if tenant == "intra":
        ManagedTenant = INTRATenant
        ManagedToken = INTRAToken
    elif tenant == "aws":
        ManagedTenant = AWSTenant
        ManagedToken = AWSToken
    elif tenant == "gcp":
        ManagedTenant = GCPTenant
        ManagedToken = GCPToken
    elif tenant == "azr":
        ManagedTenant = AZRTenant
        ManagedToken = AZRToken
    else:
        print("Error - Wrong argument")
        sys.exit(1)

    apps=[]
    actions=[]

    #0-Get Managed apps Ids
    error, all_apps = get(ManagedTenant, ManagedToken, Api["APP_WEB"]) 
    if error: 
        print("Error - Get src apps (Managed apps)")
        sys.exit(1)
    else:
        apps_json = json.loads(all_apps) #Convert String to JSON

    #1-Create file
    filename = "backup_webapps-" + ENV.lower() + "-" + tenant + ".json" 
    print("Result in: " + filename)
    with open(filename, "w") as f: 

        #For each app
        for app in apps_json['values']: 
            appId = app['id']
            appName = app['name']
            print(appId)

            #2-Backup key user actions
            error, key_user_actions = get_entity(ManagedTenant, ManagedToken, Api["APP_WEB"], appId, Api["KEY_USER_ACTION"])
            if error:
                print("Error - Get key user actions")
                sys.exit(1)
            else:
                key_user_actions_json = json.loads(key_user_actions) 

                if key_user_actions_json["keyUserActionList"] is not None: #if key user actions list is not empty
                    for action in key_user_actions_json["keyUserActionList"]:
                        actions.append(action) #Add action to the list

            #3-Backup data privacy settings object
            error, data_privacy_settings = get_settings_object(ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['DATA_PRIVACY_SETTINGS_WEB'], appId, "objectId,value,name")
            if error:
                print("Error - Get Data privacy settings object")
                sys.exit(1)
            else:
                data_privacy_settings_json = json.loads(data_privacy_settings)
                if data_privacy_settings_json['items']: #if Data privacy is not empty 
                    data_privacy_json = data_privacy_settings_json['items'][0]
                    data_privacy_list = data_privacy_json
                else:
                    data_privacy_list = {}

            #4-Backup error rules 
            error, error_rules = get_entity(ManagedTenant, ManagedToken, Api["APP_WEB"], appId, Api["ERROR_RULES"] )
            if error:
                print("Error - Get error rules settings")
                sys.exit(1)
            else:
                error_rules_json = json.loads(error_rules) 
                error_rules_list = error_rules_json

                #5-Create json structure for the backup
                app = {
                        "name" : appName,
                        "id" : appId,
                        "keyUserActionList" : actions,
                        "dataPrivacy" : data_privacy_list,
                        "errorRules": error_rules_list
                    }       
                
                #6-Add result to list
                apps.append(app) 
                actions =[]

                #Pause
                now = datetime.datetime.now()
                print("Current date and time : ")
                print(now.strftime("%Y-%m-%d %H:%M:%S"))
                time.sleep(10)

        #7-Write result into file
        json.dump(apps, f, indent=4) 
        f.close()
        print("Done writing JSON data into file.") 

if __name__ == '__main__':
    main()

#__END__
