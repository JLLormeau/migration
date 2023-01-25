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
Api ={'APP_WEB' : '/api/config/v1/applications/web', 'APP_MOBILE' : '/api/config/v1/applications/mobile', 'KEY_USER_ACTION' : '/keyUserActions', 'ERROR_RULES' : '/errorRules', 'SETTINGS_OBJECT' : '/api/v2/settings/objects', 'SETTINGS_OBJECT' : '/api/v2/settings/objects', 'MANUAL_APP': '/api/v1/rum/manualApps', 'JS_TAG': '/api/v1/rum/jsTag', 'ASYNC_CODE_SNIPPET': '/api/v1/rum/asyncCS', 'INLINE_SCRIPT': '/api/v1/rum/jsInlineScript'}
schemaIds={'DATA_PRIVACY_SETTINGS_MOBILE':'builtin:rum.mobile.privacy', 'ERROR_SETTINGS_MOBILE': 'builtin:rum.mobile.request-errors', 'CRASH_SETTINGS_MOBILE' : 'builtin:anomaly-detection.rum-mobile-crash-rate-increase', 'CRASH_SETTINGS_CUSTOM': 'builtin:anomaly-detection.rum-custom-crash-rate-increase', 'JS_UPDATES': 'builtin:rum.web.rum-javascript-updates'}

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
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_entity_script(url, token, api, entityId):
    url = url + api + "/" + entityId  #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId
    error, message = http_get_script(url, token)
    check_for_errors(error, message)
    return error, message

def get_settings_object(url, token, api, schemaIds):
    schemaIds =  schemaIds.replace(":", "%3A")
    schemaIds =  schemaIds.replace(",", "%2C")
    url = url + api + "?schemaIds=" + schemaIds
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

    error, manual_apps_managed = get(ManagedTenant, ManagedToken, Api["MANUAL_APP"])
    if error:
        print("Error - Get  manual apps (Managed")
    else:
        manual_apps_managed_json = json.loads(manual_apps_managed)

    error, manual_apps_saas = get(SaasTenant, SaasToken, Api["MANUAL_APP"])
    if error:
        print("Error - Get  manual apps (SaaS)")
    else:
            manual_apps_saas_json = json.loads(manual_apps_saas)

    not_migrated_apps = []
    cpt_managed = 0
    cpt_saas = 0
    for app in manual_apps_managed_json: 
        not_migrated_apps.append(app["displayName"])
    print(not_migrated_apps)

    #Pour toutes les applications manuelles source (Managed)
    for app in manual_apps_managed_json: 
        appId = app["applicationId"]
        app_managed = app["displayName"]
        cpt_managed += 1
        #print(app_managed)

        # Vérifier si l'application utilise la dernière version du JS
        error, js_updates_settings = get_settings_object(ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds["JS_UPDATES"])
        js_updates_settings_json = json.loads(js_updates_settings)
        js_version = js_updates_settings_json["items"][0]["value"]["JavascriptVersion"]
        print(js_version)

        #TODO Sinon update SaaS config

        #Récupérer le type d'injection
        if app_managed != "ps2":
            error, app_config = get_entity(ManagedTenant, ManagedToken, Api["APP_WEB"],appId)
            if error:
                print("Error - Get injection type")
            else:
                app_config_json = json.loads(app_config)
                injection_mode = app_config_json["monitoringSettings"]["injectionMode"]
                #print(injection_mode)

        #OUTPUT
        print(app_managed + " - JS version -> " + js_version + ", " + injection_mode)

        #Pour toutes les manual_apps_saas_json manuelles cible (SaaS)
        for app in manual_apps_saas_json: 
            appId_saas = app["applicationId"]
            app_saas = app["displayName"]

            #Récupérer les nouveaux JS
            if (injection_mode == "JAVASCRIPT_TAG") & (app_managed == app_saas):
                cpt_saas += 1        
                error, js_tag = get_entity_script(SaasTenant, SaasToken, Api["JS_TAG"], appId_saas)
                if error:
                    print("Error - Get JS tag")
                else:
                    js_script = js_tag.decode("utf-8") #Convert byte to str
                    app_name = app_saas.replace("://", "~")
                    app_name = app_name.replace("/", "~")
                    app_name = app_name.replace(":", "~")
                    filename = injection_mode + "-" + app_name + "_" + appId_saas + "_" + ENV.lower() + "-" + tenant + "--" + ENV.lower() + ".txt"
                    with open(filename, "w") as f:
                        f.write(js_script) #Write result into file
                    print("New JS tag in: " + filename)
                    not_migrated_apps.remove(app_saas)

            #Récupérer les nouveaux code snippet
            if (injection_mode == "CODE_SNIPPET") & (app_managed == app_saas):  
                cpt_saas += 1
                error, code_snippet = get_entity_script(SaasTenant, SaasToken, Api["ASYNC_CODE_SNIPPET"], appId_saas)
                if error:
                    print("Error - Get code snippet")
                else:
                    code_snippet_script = code_snippet.decode("utf-8") #Convert byte to str
                    app_name = app_saas.replace("://", "~")
                    app_name = app_name.replace("/", "~")
                    app_name = app_name.replace(":", "~")
                    filename = injection_mode + "-" + app_name + "_" + appId_saas + "_" + ENV.lower() + "-" + tenant + "--" + ENV.lower() + ".txt"
                    with open(filename, "w") as f:
                        f.write(code_snippet_script) #Write result into file
                    print("New code snippet in: " + filename)
                    not_migrated_apps.remove(app_saas)

            #Récupérer les nouveaux inline code
            if (injection_mode == "INLINE_CODE") & (app_managed == app_saas):  
                cpt_saas += 1
                error, inline_code = get_entity_script(SaasTenant, SaasToken, Api["INLINE_SCRIPT"], appId_saas)
                if error:
                    print("Error - Get inline code")
                else:
                    inline_code_script = inline_code.decode("utf-8") #Convert byte to str
                    app_name = app_saas.replace("://", "~")
                    app_name = app_name.replace("/", "~")
                    app_name = app_name.replace(":", "~")
                    filename = injection_mode + "-" + app_name + "_" + appId_saas + "_" + ENV.lower() + "-" + tenant + "--" + ENV.lower() + ".txt"
                    with open(filename, "w") as f:
                        f.write(inline_code_script) #Write result into file
                    print("New inline code in: " + filename)
                    not_migrated_apps.remove(app_saas)
    
    print("Managed applications: " + str(cpt_managed))
    print("SaaS applications: " + str(cpt_saas))
    print("Applications not downloaded: ")
    print(not_migrated_apps)
            
if __name__ == '__main__':
    main()

#__END__
