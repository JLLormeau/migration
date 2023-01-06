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
print(SaasTenant)

### Mapping
Api ={'APP_WEB' : '/api/config/v1/applications/web', 'APP_MOBILE' : '/api/config/v1/applications/mobile', 'KEY_USER_ACTION' : '/keyUserActions', 'ERROR_RULES' : '/errorRules', 'SETTINGS_OBJECT' : '/api/v2/settings/objects'}
schemaIds={'DATA_PRIVACY_SETTINGS_WEB':'builtin:preferences.privacy'}

#================================================
# Functions
#================================================

#GET
def get(url, token, api):
    url = url + api
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

#POST
def post(url, token, api, payload):
    url = url + api #Ex: "https://" + <domain> + "/api/v2/settings/objects/"
    print(url)
    error, message = http_post_validate(url, token, payload)
    check_for_errors(error, message)
    return error, message

def post_entity(url, token, api, entityId, option, payload):
    url = url + api + "/" + entityId + option #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId + "/keyUserActions"
    error, message = http_post(url, token, payload)
    check_for_errors(error, message)
    return error, message

#PUT
def put_entity(url, token, api, entityId, payload):
    url = url + api + "/" + entityId #Ex: "https://" + <domain> + "/api/v2/settings/objects/" + objectId
    error, message = http_put(url, token, payload)
    check_for_errors(error, message)
    return error, message

def put_entity_option(url, token, api, entityId, option, payload):
    url = url + api + "/" + entityId + option #Ex: "https://" + <domain> + "/api/config/v1/applications/web/" + appId + "/errorRules"
    error, message = http_put(url, token, payload)
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
            tenant = optlist[0][1] #--tenant=dev-intra

    #1-Create file
    src_file = "backup_webapps-" + ENV.lower() + "-" + tenant + ".json"
    dest_file = "import_webapps-" + ENV.lower() + "-" + tenant + "--" + ENV + ".json"

    #1-Clean backup data (Managed config)
    if os.stat(src_file).st_size != 0:
        with open(src_file, "r") as f:
            src_apps = json.load(f)
            for app in src_apps:
                for action in app["keyUserActionList"]:#Clean key user actions
                    if 'meIdentifier' in action:
                        del action['meIdentifier'] #Delete "meIdentifier" lines
                    if 'domain' in action:
                        del action['domain'] #Delete "domain" lines
        f.close()
    else:
        print("Backup file empty. Nothing to import")
        sys.exit(1)
        
    #2-Save modification in a new file
    with open(dest_file, "w") as f:      
        json.dump(src_apps, f, indent=4)  
    f.close()   
    print("Imported configs in: " + dest_file)
    
    #3-Get destination apps (SaaS apps)
    error, dest_apps = get(SaasTenant, SaasToken, Api["APP_WEB"]) 
    if error:
        print("Error - Get SaaS apps")
        sys.exit(1)
    else:
        dest_apps_json = json.loads(dest_apps)
    
    #For each destination app (SaaS apps)
    #Create a list of not migrated apps
    cpt = 0
    not_migrated_apps = []
    with open(dest_file, "r") as f:  
        src_apps = json.load(f)       
        for src_app in src_apps:
            not_migrated_apps.append(src_app['name']) 
    f.close()

    #For each destination app (SaaS apps)
    for dest_app in dest_apps_json["values"]:
        with open(dest_file, "r") as f:
            src_apps = json.load(f)  
            #For each source app (Managed apps)
            for src_app in src_apps:
                if src_app['name'] == dest_app["name"]: #If Backup app name == SaaS app name
                    cpt += 1
                    dest_app_id = dest_app["id"]
                    print(dest_app_id)

                    #4-IMPORT KEY USER ACTIONS
                    if src_app['keyUserActionList']:                    
                        for action in src_app['keyUserActionList']:  
                            payload = action
                            error, key_user_action = post_entity(SaasTenant, SaasToken, Api['APP_WEB'], dest_app_id, Api['KEY_USER_ACTION'], payload)
                            if error:
                                print("Error - Create Key user action")
                                sys.exit(1)
                    else:
                        print("-> No key user actions - No update")

                    #5-IMPORT DATA PRIVACY
                    #Get SaaS object
                    error, settings_objects_saas = get_settings_object(SaasTenant, SaasToken, Api["SETTINGS_OBJECT"], schemaIds['DATA_PRIVACY_SETTINGS_WEB'], dest_app_id, "objectId,value,name")
                    if error:
                        print("Error - Get SaaS Data privacy settings object")
                        sys.exit(1)
                    else:
                        settings_objects_saas_json = json.loads(settings_objects_saas)

                    if src_app['dataPrivacy']: #If source settings is not empty
                          
                        if settings_objects_saas_json['items']: #If destination settings is not empty  
                            objectId = settings_objects_saas_json['items'][0]['objectId']                           
                            
                            #Update SaaS object
                            payload = src_app['dataPrivacy'] #Get backup config
                            del payload['objectId']
                            error, data_privacy = put_entity(SaasTenant, SaasToken, Api["SETTINGS_OBJECT"], objectId, payload)
                            if error:
                                print("Error - Update Data privacy settings")
                                sys.exit(1)
                            else:
                                print("-> Data privacy settings updated")
                        
                        else: #If destination settings is empty
                            value = src_app['dataPrivacy'] #Get backup config
                            del value['objectId']
                            
                            #Create new settings object
                            payload = [{
                                "schemaId" : schemaIds['DATA_PRIVACY_SETTINGS_WEB'],
                                "scope": dest_app_id,
                                "value": value["value"]
                            }]
                            error, data_privacy = post(SaasTenant, SaasToken, Api["SETTINGS_OBJECT"], payload)
                            #TODO

                    else: 
                        print("-> Default Data privacy settings - No update")
                                   
                    #6-IMPORT ERROR RULES
                    payload = src_app['errorRules'] #Get backup config
                    error, error_rules = put_entity_option(SaasTenant, SaasToken, Api["APP_WEB"], dest_app_id, Api['ERROR_RULES'], payload)
                    if error:
                        print("Error - Update error rules")
                        sys.exit(1)
                    else:
                        print("-> Error rules imported")

                    #App migrated -> remove from list
                    not_migrated_apps.remove(src_app['name']) 
        f.close()

    print("Applications migrated: " + str(cpt))
    print("Applications not migrated: ")
    print(not_migrated_apps)

if __name__ == '__main__':
    main()

#__END__
