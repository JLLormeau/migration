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
Api ={'APP_WEB' : '/api/config/v1/applications/web', 'APP_MOBILE' : '/api/config/v1/applications/mobile', 'KEY_USER_ACTION' : '/keyUserActions', 'ERROR_RULES' : '/errorRules', 'SETTINGS_OBJECT' : '/api/v2/settings/objects', 'SETTINGS_OBJECT' : '/api/v2/settings/objects'}
schemaIds={'DATA_PRIVACY_SETTINGS_MOBILE':'builtin:rum.mobile.privacy', 'ERROR_SETTINGS_MOBILE': 'builtin:rum.mobile.request-errors', 'CRASH_SETTINGS_MOBILE' : 'builtin:anomaly-detection.rum-mobile-crash-rate-increase', 'CRASH_SETTINGS_CUSTOM': 'builtin:anomaly-detection.rum-custom-crash-rate-increase'}

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
    error, all_apps =  get(ManagedTenant, ManagedToken, Api["APP_MOBILE"]) 
    if error:
        print("Error - Get src apps (Managed apps)")
        sys.exit(1)
    else:
        apps_json = json.loads(all_apps) #Convert String to JSON

    #1-Create file
    filename = "backup_mobileapps-" + ENV.lower() + "-" + tenant + ".json"
    print("Result in: " + filename)
    with open(filename, "w") as f:

        #For each app
        for app in apps_json['values']:
            appId = app['id']
            appName = app['name']
            print(appId)

            #2-Backup key user actions
            error, key_user_actions = get_entity(ManagedTenant, ManagedToken, Api["APP_MOBILE"], appId, Api["KEY_USER_ACTION"])
            if error:
                print("Error - Get key user actions")
                sys.exit(1)
            else:
                key_user_actions_json = json.loads(key_user_actions)

                if key_user_actions_json["keyUserActions"] is not None: #if key user actions list is not empty
                    for action in key_user_actions_json["keyUserActions"]:
                        actions.append(action) #Add action to the list
            
            #3-Backup data privacy settings object
            if appId.startswith('MOBILE_APPLICATION-'):
                error, data_privacy_settings = get_settings_object(ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['DATA_PRIVACY_SETTINGS_MOBILE'], appId, "objectId,value,name")
                if error:
                    print("Error - Get Data privacy settings object")
                    sys.exit(1)
                else:
                    data_privacy_settings_json = json.loads(data_privacy_settings)

                    if data_privacy_settings_json['items']: #if settings is not empty 
                        data_privacy_json = data_privacy_settings_json['items'][0]
                        data_privacy_list = data_privacy_json           
                    else:
                        data_privacy_list = {}
            #if CUSTOM_APPLICATION -> No data privacy settings
            if appId.startswith('CUSTOM_APPLICATION-'):
                data_privacy_list = {}

            #4-Backup request erros rules
            error, request_errors_settings = get_settings_object(ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['ERROR_SETTINGS_MOBILE'], appId, "objectId,value,name")
            if error:
                print("Error - Get request erros rules object")
                sys.exit(1)
            else:
                request_errors_settings_json = json.loads(request_errors_settings)
            
                if request_errors_settings_json['items']: #if settings is not empty 
                    request_errors_json = request_errors_settings_json['items'][0]
                    request_errors_list = request_errors_json
                else:
                    request_errors_list = {}

            #TODO Backup anomaly detection?

            #5-Backup Crash rate increase 
            if appId.startswith('MOBILE_APPLICATION-'):
                error, crash_settings = get_settings_object(ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['CRASH_SETTINGS_MOBILE'], appId, "objectId,value,name")
                if error:
                    print("Error - Get crash settings object")
                    sys.exit(1)
                else:
                    crash_settings_json = json.loads(crash_settings)
            if appId.startswith('CUSTOM_APPLICATION-'):
                error, crash_settings = get_settings_object(ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['CRASH_SETTINGS_CUSTOM'], appId, "objectId,value,name")
                if error:
                    print("Error - Get crash settings object")
                    sys.exit(1)
                else:
                    crash_settings_json = json.loads(crash_settings)

            if crash_settings_json['items']: #if settings is not empty 
                crash_settings_json = crash_settings_json['items'][0]
                crash_list = crash_settings_json
            else:
                crash_list = {}

            #6-Create json structure for the backup
            app = {
                    "name" : appName,
                    "id" : appId,
                    "keyUserActionList" : actions,
                    "dataPrivacy" : data_privacy_list,
                    "requestErrorsList": request_errors_list,
                    "crash_list": crash_list
                }     
            
            #7-Add result to list
            apps.append(app)

        #7-Write result into file
        json.dump(apps, f, indent=4)
        f.close()
            
        print("Done writing JSON data into file.") 

if __name__ == '__main__':
    main()

#__END__
