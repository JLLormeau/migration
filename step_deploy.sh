#!/bin/bash
echo "################"
echo script_name ${0##*/}
. env.sh

mkdir -p log/$env >/dev/null 2>&1

step=$1
#echo env= $env
TIME=`date +%Y%m%d%H%M%S`
log=log/"$env"/deploy_"$env"_"$tenant"_"$step"_"$TIME".log

{
date
echo $step
echo
#echo fix_deploy
#./fix_deploy.sh

for api in  `cat $step | grep -v "#"`
do
   echo "#####################"
   echo "API="$api
   echo "#####################"
   echo
   ./del_doublon.sh $api
   ./script_monaco.sh $api
done


echo
date
echo "##"$step"##################################"
cat $log | grep RESULTAT_DEPLOY 
}| tee $log
