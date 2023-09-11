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
schemaIds={'HOST_MONITORING':'builtin:host.monitoring','CONTAINER_TECHNOLOGY':'builtin:container.technology','DISK_OPTIONS':'builtin:disk.options','DISK_EXTENSION':'builtin:disk.analytics.extension','NETTRACER':'builtin:nettracer.traffic','NETWORK_TRAFFIC':'builtin:exclude.network.traffic','PG_MONITORING':'builtin:host.process-groups.monitoring-state','PG_FLAGS':'builtin:process-group.detection-flags','DECLARATIVE_PROCESS_MONITORING':'builtin:declarativegrouping','PROCESS_AVAILABILITY':'builtin:processavailability','PROCESS_SNAPSHOT':'builtin:process-visibility','ANOMALY_DETECTION_INFRASTRUCTURE':'builtin:anomaly-detection.infrastructure-hosts','ANOMALY_DETECTION_DISK':'builtin:anomaly-detection.infrastructure-disks','OA_UPDATES':'builtin:deployment.oneagent.updates','OS_SERVICES':'builtin:os-services-monitoring','ECC':'builtin:eec.local','LOG_OA_CONFIG':'builtin:logmonitoring.log-agent-configuration','CUSTOM_LOG':'builtin:logmonitoring.custom-log-source-settings','LOG_STORAGE':'builtin:logmonitoring.log-storage-settings','LOG_TIMESTAMP':'builtin:logmonitoring.timestamp-configuration'}


#================================================
# Functions
#================================================

def get_entity(url, token, api, entityId, option):
    url = url + api + "/" + entityId + option #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId + "/keyUserActions"
    error, message = http_get(url, token)
    #print(url)
    check_for_errors(error, message)
    return error, message

def get_entity(url, token, api, entityId):
    url = url + api + "/" + entityId  #Ex: "https://" + <domain> + "/api/config/v1/applications/web/"" + appId + "/keyUserActions"
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_entity_selector(url, token, api, selector):
    url = url + api + "?entitySelector=" + selector #entitySelector=type%28%22HOST%22%29%2ChealthState%28%22HEALTHY%22%29
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_settings_object(url, token, api, schemaIds, fields):
    schemaIds =  schemaIds.replace(":", "%3A")
    schemaIds =  schemaIds.replace(",", "%2C")
    fields =  fields.replace(",", "%2C")
    url = url + api + "?schemaIds=" + schemaIds + "&fields=" + fields + "&pageSize=500&author"
    #print(url)
    error, message = http_get(url, token)
    check_for_errors(error, message)
    return error, message

def get_settings_object_scopes(url, token, api, schemaIds, fields, scopes):
    schemaIds =  schemaIds.replace(":", "%3A")
    schemaIds =  schemaIds.replace(",", "%2C")
    fields =  fields.replace(",", "%2C")
    url = url + api + "?schemaIds=" + schemaIds + "&fields=" + fields + "&pageSize=500" + "&scopes=" + scopes
    #print(url)
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
        #1-For each host, get hostId 
        selector = "type%28%22HOST%22%29%2ChealthState%28%22HEALTHY%22%29"
        error,entities = get_entity_selector(url, token, Api["ENTITY"], selector)
        if error:
            print("Error - Get list host healthy")
        else:
            entities_json = json.loads(entities)
            #print(entities_json)
            for entity in entities_json["entities"]:
                entityName = entity["displayName"]
                hostId = entity["entityId"]
                #print(entityName)
                #3-Get Settings object for each host
                error, settings_object = get_settings_object_scopes(url, token, Api["SETTINGS_OBJECT"], schema, "scope,value", hostId)
                
                if error:
                    print("Error - Get settings object")
                    errors.append(entityName)
                else:
                    settings_object_json = json.loads(settings_object)
                    if settings_object_json['items']: #if Object is not empty 
                        for object in settings_object_json['items']: #Add each object to list
                            cpt = cpt + 1
                            settings_object_json = object
                            #hostId = settings_object_json['scope']
                            value = settings_object_json['value']

                            #2- Get Hostgroup
                            error,host_entity = get_entity(url, token, Api['ENTITY'], hostId)
                            if error:
                                print("Error - Get host entity")
                                errors.append(entityName)
                                #print(host_entity)
                            else:
                                host_entity_json = json.loads(host_entity)
                                if 'isInstanceOf' in host_entity_json['fromRelationships']:
                                    hostGroupEntityName = host_entity_json['fromRelationships']['isInstanceOf'][0]['id']
                                    #print(hostGroupEntityName)
                                else:
                                    hostGroupEntityName = "no hostGroup"

                                #4-Create json structure for the backup
                                object = {
                                        "schemaId" : schema,
                                        "scope" : hostId,
                                        "value" : value,
                                        "entityName" : entityName,
                                        "HOST_GROUP_entityName": hostGroupEntityName,
                                        "status":"to import"
                                    }
                                            
                                #5-Add result to list and create csv mapping
                                objects.append(object) 
                                #print(object)
                                print(entityName + ";" + hostId + ";" + hostGroupEntityName  )     
                                
                    else:
                        #print(entityName + ": No settings to migrate")
                        continue
        
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

    print("\n//---HOST_MONITORING--//")
    filename = "backup_host-HOST_MONITORING-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['HOST_MONITORING'], filename)
    
    print("\n//---CONTAINER_TECHNOLOGY--//")
    filename = "backup_host-CONTAINER_TECHNOLOGY-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['CONTAINER_TECHNOLOGY'], filename)
    
    print("\n//---DISK_OPTIONS--//")
    filename = "backup_host-DISK_OPTIONS-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['DISK_OPTIONS'], filename)
    
    print("\n//---DISK_EXTENSION--//")
    filename = "backup_host-DISK_EXTENSION-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['DISK_EXTENSION'], filename)
    
    print("\n//---NETTRACER--//")
    filename = "backup_host-NETTRACER-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['NETTRACER'], filename)
    
    print("\n//---NETWORK_TRAFFIC--//")
    filename = "backup_host-NETWORK_TRAFFIC-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['NETWORK_TRAFFIC'], filename)
    
    print("\n//---PG_MONITORING--//")
    filename = "backup_host-PG_MONITORING-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PG_MONITORING'], filename)
    
    print("\n//---PG_FLAGS--//")
    filename = "backup_host-PG_FLAGS-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PG_FLAGS'], filename)
    
    print("\n//---DECLARATIVE_PROCESS_MONITORING--//")
    filename = "backup_host-DECLARATIVE_PROCESS_MONITORING-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['DECLARATIVE_PROCESS_MONITORING'], filename)
    
    print("\n//---PROCESS_AVAILABILITY--//")
    filename = "backup_host-PROCESS_AVAILABILITY-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_AVAILABILITY'], filename)
    
    print("\n//---PROCESS_SNAPSHOT--//")
    filename = "backup_host-PROCESS_SNAPSHOT-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['PROCESS_SNAPSHOT'], filename)
    
    print("\n//---ANOMALY_DETECTION_INFRASTRUCTURE--//")
    filename = "backup_host-ANOMALY_DETECTION_INFRASTRUCTURE-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['ANOMALY_DETECTION_INFRASTRUCTURE'], filename)
    
    print("\n//---ANOMALY_DETECTION_DISK--//")
    filename = "backup_host-ANOMALY_DETECTION_DISK-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['ANOMALY_DETECTION_DISK'], filename)
    
    print("\n//---OA_UPDATES--//")
    filename = "backup_host-OA_UPDATES-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['OA_UPDATES'], filename)
    
    print("\n//---OS_SERVICES--//")
    filename = "backup_host-OS_SERVICES-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['OS_SERVICES'], filename)
    
    print("\n//---ECC--//")
    filename = "backup_host-ECC-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['ECC'], filename)
    
    print("\n//---LOG_OA_CONFIG--//")
    filename = "backup_host-LOG_OA_CONFIG-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['LOG_OA_CONFIG'], filename)
    
    print("\n//---CUSTOM_LOG--//")
    filename = "backup_host-CUSTOM_LOG-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['CUSTOM_LOG'], filename)
    
    print("\n//---LOG_STORAGE--//")
    filename = "backup_host-LOG_STORAGE-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['LOG_STORAGE'], filename)
    
    print("\n//---LOG_TIMESTAMP--//")
    filename = "backup_host-LOG_TIMESTAMP-" + ENV.lower() + "-" + tenant + ".json"
    backup_settings (ManagedTenant, ManagedToken, Api["SETTINGS_OBJECT"], schemaIds['LOG_TIMESTAMP'], filename)
    


if __name__ == '__main__':
    main()

#__END__
