#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

apiUpper=$1
api="${apiUpper,,}"
log=$env/$apiUpper/"deploy_monaco_"$api.log
echo $log

echo -n "" > RELOAD

for tenant2 in GCP INTRA AZR AWS
do 
  if [ -e $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml ]
  then
    test=` cat $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml| grep "^-" | grep -ve "- name" | wc -l`
    if [ "$test" -eq  0 ]
      then
        mv $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml.skipped
      fi
  fi

done

if [ $tenant != ALL ]
then
  echo monaco deploy on $env"_"$tenant
  ./monaco deploy -e=saas_env.yaml -c $env/$apiUpper/$env"_"$tenant  |tee $log
else
  echo monaco deploy on $env
  ./monaco deploy -e=saas_env.yaml -c $env/$apiUpper  |tee $log
fi


value1=`cat $log | grep "1: "$env | cut -d "(" -f 2 | cut -d " " -f 1`
value2=`cat $log | grep "2: "$env | cut -d "(" -f 2 | cut -d " " -f 1`
value3=`cat $log | grep "3: "$env | cut -d "(" -f 2 | cut -d " " -f 1`
value4=`cat $log | grep "4: "$env | cut -d "(" -f 2 | cut -d " " -f 1`
error=`cat $log | grep "ERROR Deployment to" | cut -d " " -f 9`
value=$(( value1 + value2 + value3 + value4 ))
deploy=$((value-error))
echo

if [ -z $error ]
then
   resultmonaco=`tail -1 $log | cut -d " " -f 3`
   echo $resultmonaco
   if [ $resultmonaco !=  INFO ]
   then 
      error=$resultmonaco
   else
      #echo $resultmonaco
      export error=0
      echo $apiUpper >> RELOAD

   fi
else

 Responsibles=`cat $log | grep responsible | grep -oE '[^ ]+$' | sort | uniq`
 for tenant2 in GCP AWS AZR INTRA
 do
  if [ $error -eq 0 ] 
  then 
    if [ -f $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml ]
    then
      mv $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml.done
    fi
  else
    if [  `echo $Responsibles|wc -c` > 1 ]
    then
      if [ -f $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml ]
      then
        #cp $env/$apiUpper/$env"_"$tenant/$api/$api.yaml $env/$apiUpper/$env"_"$tenant/$api/$api.yaml.copy
        sed -i 's/^\- /#ok\- /g' $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml
        sed -i 's/^#ok\- name/\- name/g' $env/$apiUpper/$env"_"$tenant2/$api/$api.yaml

      fi
    fi 
  fi

 done

 for responsible in $Responsibles 
 do
  issue=`echo $responsible |  cut -d "/" -f 5 | cut -d "." -f 1`
  tenantissue=`echo $responsible |  cut -d "/" -f 3` 
  echo "ERROR;"$apiUpper";"$issue";"$tenantissue";"$env/$apiUpper/$tenantissue/$api/$api.yaml
  sed -i "s/^#ok\- $issue/\- $issue/g" $env/$apiUpper/$tenantissue/$api/$api.yaml
 done

fi

val=`cat $env/$apiUpper/differ_$api.log| wc -l`

echo API=$apiUpper=RESPONSIBLE_ERROR=`echo $Responsibles`
echo API=$apiUpper=DOUBLON_DIFFER=$val
echo API=$apiUpper=DEPLOY=$deploy
echo API=$apiUpper=ERROR=$error
echo API=$apiUpper=RESULTAT_DEPLOY=$val=$deploy=$error

#for tenant in AZR GCP AWS INTRA
#do
#mv $env/$apiUpper/$env"_"$tenant/$api/$api.yaml.skipped $env/$apiUpper/$env"_"$tenant/$api/$api.yaml
#if [ -f "$env/$apiUpper/$env"_"$tenant/$api/$api.yaml" ]
#  then
#   sed -i 's/^#ok\- /\- /g' $env/$apiUpper/$env"_"$tenant/$api/$api.yaml
#fi
#done
