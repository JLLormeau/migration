#!/bin/bash
TIME=`date +%Y%m%d%H%M%S`
DIR=/root/DEV/migration
log=$DIR/log/cron_"$TIME".log
. $DIR/env.sh
export tenant=ALL

echo "##"
echo script_name ${0##*/}
cd $DIR
python3 Mapping_Entity.py
export local_rep=DASHBOARD-V2
{
echo $TIME
echo $local_rep
./monaco download -e=saas_env.yaml -p=dashboard-v2 $local_rep
./mapping_entity.sh
./monaco deploy -e=saas_env.yaml -c $local_rep/Saas
echo $TIME
}| tee $log
