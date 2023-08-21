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
Api ={'SETTINGS_OBJECT' : '/api/v2/settings/objects', 'ENTITY': '/api/v2/entities/'}
schemaIds={'PROCESS_GROUP_RUM':'builtin:rum.processgroup','PROCESS_GROUP_DEEP_MONITORING':'builtin:process-group.monitoring.state','PROCESS_GROUP_OA_FEATURES':'builtin:oneagent.features','PROCESS_GROUP_AVAILABILITY':'builtin:availability.process-group-alerting','PROCESS_GROUP_CONNECTIVITY':'builtin:alerting.connectivity-alerts'}


#================================================
# Functions
#================================================

def get_entity(url, token, api, entityId, option):
    url = url + api + "/" + entityId + option #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId + "/keyUserActions"
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_entity(url, token, api, entityId):
    url = url + api + "/" + entityId  #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId + "/keyUserActions"
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_settings_object(url, token, api, schemaIds, fields):
    schemaIds =  schemaIds.replace(":", "%3A")
    schemaIds =  schemaIds.replace(",", "%2C")
    fields =  fields.replace(",", "%2C")
    url = url + api + "?schemaIds=" + schemaIds + "&fields=" + fields + "&pageSize=500&author"
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

#================================================
# Main
#================================================

#Backup service settings object
def backup_settings (url, token, api, schema, filename):
    objects=[]
    errors=[]
    
    print("Result in: " + filename)

    #0-Create backup file
    with open(filename, "w") as f: 
        cpt = 0

        #1-Get Settings object
        error, settings_object = get_settings_object(url, token, api, schema,"scope,value")
        if error:
            print("Error - Get settings object")
            errors.append(schema)
        else:
            settings_object_json = json.loads(settings_object)
            if settings_object_json['items']: #if Object is not empty 

                for object in settings_object_json['items']: #Add each object to list
                    cpt = cpt + 1
                    settings_object_json = object
                    serviceId = settings_object_json['scope']
                    value = settings_object_json['value']

                    #2-Get entity Name
                    if serviceId != "environment":
                        error,entity = get_entity(url, token, Api["ENTITY"], serviceId)
                        if error:
                            print("Error - Get entity Name")
                            errors.append(serviceId)

                        else:
                            entity_json = json.loads(entity)
                            entityName = entity_json['displayName'] 

                            #3-Get serviceId, entityName, HOST_GROUP_entityName
                            if 'isHostGroupOf' in entity_json['toRelationships']:
                                hostGroupId = entity_json['toRelationships']['isHostGroupOf'][0]['id']
                                error,entity = get_entity(url, token, Api["ENTITY"], hostGroupId)
                                if error:
                                    print("Error - Get relationship entity")
                                    errors.append(serviceId)
                                else:
                                    entity_json = json.loads(entity)
                                    hostGroupEntityName = entity_json['displayName']

                                    #4-Create json structure for the backup
                                    object = {
                                            "schemaId" : schema,
                                            "scope" : serviceId,
                                            "value" : value,
                                            "entityName" : entityName,
                                            "HOST_GROUP_entityName": hostGroupEntityName,
                                            "status":"to import"
                                        }
                                    
                                    #5-Add result to list and create csv mapping
                                    objects.append(object) 
                                    print(entityName + ";" + serviceId + ";" + hostGroupEntityName  + ";" + hostGroupId) 

                            else:
                                #4 bis-Create json structure for the backup if error
                                object = {
                                        "schemaId" : schema,
                                        "scope" : serviceId,
                                        "value" : value,
                                        "entityName" : entityName,
                                        "HOST_GROUP_entityName": "host not running anymore",
                                        "status":"to import"
                                    }
                                
                                #5 bis-Add result to list and create csv mapping
                                objects.append(object) 
                                print(entityName + ";" + serviceId)       
                            
                    else:
                        key_request_list = {}
            
            #6-Write result into file
            json.dump(objects, f, indent=4) 
            f.close()
            print("Done writing JSON data into file.") 
            print("Count: ")
            print(cpt)
            print("Settings object not backed up: ")
            print(errors)


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

    print("\n//---RUM--//")
    filename = "backup_pg_rum-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_GROUP_RUM'], filename)
    
    print("\n//---Deep monitoring--//")
    filename = "backup_pg_deep_monitoring-" + ENV.lower() + "-" + tenant + ".json" 
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_GROUP_DEEP_MONITORING'], filename)


    print("\n//---OA features--//")
    filename = "backup_pg_oa_features-" + ENV.lower() + "-" + tenant + ".json" 
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_GROUP_OA_FEATURES'], filename)

    print("\n//---Availability--//")
    filename = "backup_pg_availability-" + ENV.lower() + "-" + tenant + ".json" 
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_GROUP_AVAILABILITY'], filename)
    
    print("\n//---Connectivity--//")
    filename = "backup_pg_connectivity-" + ENV.lower() + "-" + tenant + ".json" 
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_GROUP_CONNECTIVITY'], filename)

if __name__ == '__main__':
    main()

#__END__
