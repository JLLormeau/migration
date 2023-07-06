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

bf_mapping.csv

    bf_source;bf_cible;
    
Select a specific env pour le mapping (optionnal)

    export tenant=AWS|GCP|AZR|INTRA|ALL
    
Git clone

    git clone https://github.com/JLLormeau/migration
    cd migration
    chmod +x *.sh monaco

Prerequisite

    . env.sh
    ./monaco download -e=managed_env.yaml $directory_source
    
  Or for a specific env
    
    ./monaco download -e=managed_env.yaml -s=$tenant $directory_source
    
Relaod API (if error or missing)

    ./monaco download -e=managed_env.yaml -s=$tenant -p=<api> $directory_source
    
FIX DEV

    ./fix_deploy.sh

Monaco STEP 1

    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    ./reorganize.sh
    ./step_deploy.sh ALL
    export local_rep=$env
    python3 Mapping_Config.py
    ./mapping_config.sh
    ./mapping_bf.sh
    ./adjust-config-azure-credential.sh
    ./adjust-config-gcp-credential.sh
    ./clean-config-aws-credential.sh
    ./clean-id-application-mobile.sh
    ./clean-id-application-web.sh
    ./clean-order-service-opaque.sh
    ./dashboard-constraint-violated.sh log/$env/deploy_$env_ALL_<date>.log => action manuelle 
    
    ./step_deploy.sh ALL

Monaco STEP 2
    
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    ./step_deploy.sh STEP2
    
Mapping Owner (fichier owner_mapping.csv)
 
    . env.sh
    python3 Mapping_Owner.py (ou récupérér fichier owner_mapping.csv)
 
Mapping Entity (à faire avant la migration des entités sur le Saas - génère les fihciers CSV d'entité managed)
 
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    python3 Mapping_Entity.py
 
Mapping Dashboard (multiples itérations)
    
    . env.sh   
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=DASHBOARD-V2
    ./monaco download -e=saas_env.yaml -p=dashboard-v2 $local_rep
    cp -r $local_rep backup/$local_rep
    ./mapping_owner.sh
    ./mapping_url.sh
    ./mapping_config.sh
    ./monaco deploy -e=saas_env.yaml -c $local_rep/Saas

############### Validation ###############

Validate Config

    . env.sh
    python3 Validate_Config.py
    
############### Mapping Entity ###############

Mapping Entity (à refaire une fois les entités migrées sur le Saas - peut-être plusieurs fois - permet de faire le mapping entre Saas et Managed)
 
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    python3 Mapping_Entity.py

Mapping Dashboard (multiples itérations)
    
    . env.sh   
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=DASHBOARD-V2
    ./monaco download -e=saas_env.yaml -p=dashboard-v2 $local_rep
    cp -r $local_rep backup/$local_rep
    ./mapping_entity.sh
    ./monaco deploy -e=saas_env.yaml -c $local_rep/Saas


Mapping CALCULATED-METRICS-LOG (entityid)
    
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=./$env/CALCULATED-METRICS-LOG
    cp -r local_rep backup/CALCULATED-METRICS-LOG
    ./mapping_entity.sh
    ./script_monaco.sh CALCULATED-METRICS-LOG
 
 Mapping REQUEST-ATTRIBUTES (entityid)
    
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=./$env/REQUEST-ATTRIBUTES
    cp -r local_rep backup/REQUEST-ATTRIBUTES
    ./mapping_entity.sh
    ./script_monaco.sh REQUEST-ATTRIBUTES
   
Mapping SYNTHETIC-MONITOR (configuration id)
    
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=./$env/SYNTHETIC-MONITOR
    cp -r local_rep backup/SYNTHETIC-MONITOR
    ./mapping_config.sh
    ./script_monaco.sh SYNTHETIC-MONITOR

Mapping SYNTHETIC-MONITOR (for DEV only)
    
    . env.sh   
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=./$env/SYNTHETIC-MONITOR
    cp -r local_rep backup/SYNTHETIC-MONITOR
    ./mapping_synthetic.sh
    ./script_monaco.sh SYNTHETIC-MONITOR
    
Mapping SLO (configuration id)
    
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=./$env/SLO
    cp -r local_rep backup/SLO
    ./mapping_entity.sh
    ./script_monaco.sh SLO   

Mapping Key Request (a faire)
    
    . env.sh
    export tenant=AWS|GCP|AZR|INTRA|ALL
    export local_rep=backup_keyRequest-[ENV]-[TENANT].json
    python3 Backup_KeyRequest_config.py 
    ./mapping_entity.sh
    python3  Post_Settings_Object_PayloadFile.py backup_keyRequest-[ENV]-[TENANT].json

Mapping beacon

    . env.sh   
    export local_rep=BEACON
    ./monaco download -e=saas_env.yaml -p=application-web,application-mobile $local_rep
    ./mapping_bf.sh
    ./monaco deploy -e=saas_env.yaml -c $local_rep/Saas

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


