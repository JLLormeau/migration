#!/bin/bash
. env.sh

step=$1
echo env= $env
TIME=`date +%Y%m%d%H%M%S`
log="log/"$env"/deploy_"$env"_"$step"_"$TIME.log
difflog="log/"$env"/diff_"$env"_"$step"_"$TIME.log

{
date
echo $step
echo
#echo fix_deploy
#./fix_deploy.sh
echo $TIME > $difflog

for api in  `cat $step | grep -v "#"`
do
   echo "#####################"
   echo "API="$api
   echo "#####################"
   echo
   ./del_doublon.sh $api
   ./script_monaco.sh $api
done

cat `find ./$env/* -name differ*.log` >> $difflog

echo
date
echo "##"$step"##################################"
cat $log | grep RESULTAT_DEPLOY 
}| tee $log
