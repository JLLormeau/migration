# Migration

Variables env.sh
    
    #ENV = DEV | RE7 | OPE
    export env=
    export NEW_CLI=1
    export directory_source=Deploy-$env-source
    #Saas ENV
    export SaasTenant=
    export SaasToken=
    #Managed ENV
    export Cluster=
    export ClusterToken=
    export GCPTenant=
    export GCPToken=
    export AWSTenant=
    export AWSToken=
    export INTRATenant=
    export INTRAToken=
    export AZRTenant=
    export AZRToken=
    
Git clone

    git clone https://github.com/JLLormeau/migration
    cd migration
    chmod +x *.sh monaco

Prerequisite

    . env.sh
    ./monaco download -e=managed_env.yaml $directory_source
    
Relaod APi (if error or missing)

    ./monaco download -e=managed_env.yaml -s=<ENV> -p=<api> $directory_source
    
FIX DEV

    ./fix_deploy.sh

Monaco STEP 1

    ./reorganize.sh
    ./step_deploy.sh ALL
    . env.sh
    python3 Mapping_Config.py
    ./mapping.sh
    ./adjust-config-azure-credential.sh
    ./adjust-config-gcp-credential.sh
    ./clean-config-aws-credential.sh
    ./clean-id-application-mobile.sh
    ./clean-id-application-web.sh
    ./clean-order-service-opaque.sh
    ./dashboard-constraint-violated.sh log/$env/deploy_$env_ALL_<date>.log => action manuelle 

Monaco STEP 2
 
    ./step_deploy.sh STEP2
    
Mapping Owner (fichier owner_mapping.csv)
 
    . env.sh
    python3 Mappingt_Owner.py (ou récupérér fichier owner_mapping.csv)
 
 
Mapping Entity (à faire avant la migration des entités sur le Saas - génère les fihciers CSV d'entité managed)
 
    . env.sh
    python3 Mappingt_Entity.py
 
Mapping Dashboard (multiples itérations)
    
    . env.sh   
    export api_saas=DASHBOARD-V2
    ./monaco download -e=saas_env.yaml -p=dashboard-v2 $api_saas
    cp -r $api_saas backup/$api_saas
    ./mapping_owner.sh
    ./mapping_url.sh
    ./mapping_config.sh
    ./monaco deploy -e=saas_env.yaml -c $api_saas/Saas

############### Validation ###############

Validate Config

    . env.sh
    python3 Validate_Config.py
    
############### Mapping Entity ###############

Mapping Entity (à refaire une fois les entités migrées sur le Saas - peut-être plusieurs fois - permet de faire le mapping entre Saas et Managed)
 
    . env.sh
    python3 Mapping_Entity.py

Mapping Dashboard (multiples itérations)
    
    . env.sh   
    export api_saas=DASHBOARD-V2
    ./monaco download -e=saas_env.yaml -p=dashboard-v2 $api_saas
    cp -r $api_saas backup/$api_saas
    ./mapping_entity.sh
    ./monaco deploy -e=saas_env.yaml -c $api_saas/Saas

Mapping CALCULATED-METRICS-LOG (entityid)
    
    . env.sh
    export api_saas=./$env/CALCULATED-METRICS-LOG
    cp -r api_saas backup/CALCULATED-METRICS-LOG
    ./mapping_entity.sh
    ./script_monaco.sh CALCULATED-METRICS-LOG
 
 Mapping REQUEST-ATTRIBUTES (entityid)
    
    . env.sh
    export api_saas=./$env/REQUEST-ATTRIBUTES
    cp -r api_saas backup/REQUEST-ATTRIBUTES
    ./mapping_entity.sh
    ./script_monaco.sh REQUEST-ATTRIBUTES
   
Mapping SYNTHETIC-MONITOR (configuration id)
    
    . env.sh
    export api_saas=./$env/SYNTHETIC-MONITOR
    cp -r api_saas backup/SYNTHETIC-MONITOR
    ./mapping_config.sh
    ./script_monaco.sh SYNTHETIC-MONITOR
    
Mapping SLO (configuration id)
    
    . env.sh
    export api_saas=./$env/SLO
    cp -r api_saas backup/SLO
    ./mapping_entity.sh
    ./script_monaco.sh SLO   

############### Update script ###############

Re-download script
    
    git reset --hard HEAD
    git pull
    chmod +x *.sh monaco

############### Advanced RUM config ###############

Backup Managed configurations:

    py backup_webapps_config.py --tenant=<intra, aws, gcp or azr>
    py backup_mobileapps_config.py --tenant=<intra, aws, gcp or azr>


Re-import the configuration to SaaS:

    py import_webapps_config.py --tenant=<intra, aws, gcp or azr>
    py import_mobileapps_config.py --tenant=<intra, aws, gcp or azr>

############### Generate new SaaS JS code for Agentless applications ###############

    py get_new_agentless_code.py --tenant=<intra, aws, gcp or azr>


