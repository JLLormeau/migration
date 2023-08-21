import sys
import json
import urllib.parse
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

#================================================
# Functions
#================================================

def get_entity_selector(url, token, api, entitySelector):
    entitySelector =  urllib.parse.quote_plus(entitySelector)
    url = url + api + "?entitySelector=" + entitySelector 
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def post_settings_object(url, token, body):
    url = url + "/api/v2/settings/objects?validateOnly=false"
    error, message = http_post_validate(url, token, body)
    check_for_errors(error, message)
    return error, message

#================================================
# Main functions
#================================================

def import_settings(url, token, tenant, s, option):

    src_file = "backup_" + s + "-" + ENV.lower() + "-" + tenant + ".json"
    dest_file = "import_" + s + "-" + ENV.lower() + "-" + tenant + "--" + ENV + ".json"

    print("Result in: " + dest_file)

    #1-Clean backup data (Managed config)
    not_unique = []
    if os.stat(src_file).st_size != 0:
        with open(src_file, "r") as f:
            src_settings_objects = json.load(f)
            for object in src_settings_objects:
                
                # Test si le service name est unique dans le saas":
                objectName = object['entityName'] 
                objectID = object['scope'] 
                error, entity = get_entity_selector(url, token, "/api/v2/entities", 'type("SERVICE"),entityName.equals("' + objectName + '")')
                if error:
                    print("Error - Test si le service name est unique dans le saas")
                else:
                    entity_json = json.loads(entity)
                    totalCount = entity_json['totalCount']

                    if totalCount <= 1 : # Si unique, importer
                        del object['entityName'] 
                        if option == "service":
                            del object['PROCESS_GROUP_entityName']
                            del object['HOST_GROUP_ID']
                            del object['status']
                        elif option == "process":
                            del object['HOST_GROUP_entityName']
                            del object['status']
                    else: # Si non, ne pas importer
                        object['status']="not imported because not unique"
                        not_unique.append(objectID)
        print("-> Not imported because not unique: ")
        print(len(not_unique))
        print(not_unique)
        f.close()
    else:
        print("Error - Backup file empty. Nothing to import")
        sys.exit(1)

    #2-Save modification in a new file
    with open(dest_file, "w") as f:      
        json.dump(src_settings_objects, f, indent=4)  
    f.close()   

    #3-Create new settings objects (SaaS)
    # For each object, Create a list of not migrated request
    cpt = 0
    not_migrated_objects = []
    with open(dest_file, "r") as f:  
        src_objects = json.load(f)       
        for object in src_objects:
            not_migrated_objects.append(object['scope']) 
    f.close()

    #4-IMPORT OBJECT
    object_errors = []

    with open(dest_file, "r") as f:  
        src_objects = json.load(f)       
        for object in src_objects:
            if "status" in object: # not imported because not unique
                continue
            else:
                body = [object]
                error, settings_object = post_settings_object(SaasTenant, SaasToken, body)
                if error:
                    print("Error - IMPORT OBJECT " + s)
                    object_errors.append(object["scope"])
                
                cpt = cpt +1
                print("-> " + s + " imported")
    print("Settings migrated: ")
    print(cpt)
    f.close()

def main():

    #Get arguments
    try: 
        optlist, args = getopt.getopt(sys.argv[1:], 'x', ['option=','tenant='])
        #print ('Argument list:') 
        #print(optlist) 
        #print(args)

    except getopt.GetoptError as err: # print help information and exit:
        print(err)  # will print something like "option -a not recognized"

    #Parse arguments
    for arg, value in optlist:
        if arg == '--option':
            option = optlist[0][1] 
        elif arg == '--tenant':
            tenant = optlist[1][1] 

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

    #IMPORT SETTINGS OBJECT
    #Create a loop to import all settings
    
    if option == "service":
        settings = {"service_key_requests":"builtin:settings.subscriptions.service", "service_muted_requests":"builtin:settings.mutedrequests", "service_http_failure_detection":"builtin:failure-detection.service.http-parameters", "service_general_failure_detection":"builtin:failure-detection.service.general-parameters"}
    elif option == "process":
        settings = {"pg_connectivity":"builtin:alerting.connectivity-alerts", "pg_availability":"builtin:availability.process-group-alerting", "pg_oa_features":"builtin:oneagent.features", "pg_deep_monitoring":"builtin:process-group.monitoring.state"}

    for s in settings:
        print("\n /---Import: " + s + "---/")
        import_settings(SaasTenant, SaasToken, tenant, s, option)
        

if __name__ == '__main__':
    main()

#__END__
