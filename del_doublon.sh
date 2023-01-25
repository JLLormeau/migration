#!/bin/bash

echo "##"
echo script_name ${0##*/}
. env.sh

#echo env=$env
apiUpper=$1
api="${apiUpper,,}"
#ls $env/$apiUpper/$env"_GCP"/$api/$api.yaml



for doublon in differ identical
do
  echo $doublon
  cd $env/$apiUpper
  echo  "diff -sarq $env"_GCP" $env"_INTRA" | grep Files | grep .json | grep $doublon "
  diff -sarq $env"_GCP" $env"_AZR" | grep Files | grep .json | grep $doublon  > doublon_p1.tmp
  diff -sarq $env"_AWS" $env"_AZR" | grep Files | grep .json | grep $doublon  >> doublon_p1.tmp
  diff -sarq $env"_INTRA" $env"_AZR" | grep Files | grep .json | grep $doublon  >> doublon_p1.tmp
  diff -sarq $env"_GCP" $env"_INTRA" | grep Files | grep .json | grep $doublon  > doublon_p2.tmp
  diff -sarq $env"_AWS" $env"_INTRA" | grep Files | grep .json | grep $doublon  >> doublon_p2.tmp
  diff -sarq $env"_GCP" $env"_AWS" | grep Files | grep .json | grep $doublon  > doublon_p3.tmp
  cat doublon_p1.tmp > $doublon"_"$api.log
  cat doublon_p2.tmp >> $doublon"_"$api.log
  cat doublon_p3.tmp >> $doublon"_"$api.log
  cd ../..

  cat $env/$apiUpper/doublon_p3.tmp | cut -d / -f 3 | cut -d . -f 1 | sort | uniq > $env/$apiUpper/doublon_p3_uniq.tmp
  cat $env/$apiUpper/doublon_p2.tmp | cut -d / -f 3 | cut -d . -f 1 | sort | uniq > $env/$apiUpper/doublon_p2_uniq.tmp
  cat $env/$apiUpper/doublon_p1.tmp | cut -d / -f 3 | cut -d . -f 1 | sort | uniq > $env/$apiUpper/doublon_p1_uniq.tmp

  if [ -e $env/$apiUpper/$env"_AZR"/$api/$api.yaml ]
  then
    for i in `cat $env/$apiUpper/doublon_p3_uniq.tmp`
      do
      if [[ -n $i ]]
      then
       sed -i "s/^\- $i/##\-$doublon"_azr" $i/g" $env/$apiUpper/$env"_AZR"/$api/$api.yaml
      fi    
    done
  fi
  echo $env"_AZR with GCP AWS INTRA"="`cat $env/$apiUpper/$doublon"_"$api.log|grep "and "$env"_AZR"| wc -l`"

  if [ -e $env/$apiUpper/$env"_INTRA"/$api/$api.yaml ]
  then
    for i in `cat $env/$apiUpper/doublon_p2_uniq.tmp`
      do
      if [[ -n $i ]]
      then
      sed -i "s/^\- $i/##\-$doublon"_intra" $i/g" $env/$apiUpper/$env"_INTRA"/$api/$api.yaml
      fi
    done
    sed -i "s/##\-$doublon"_intra" name:/\- name:/g" $env/$apiUpper/$env"_AZR"/$api/$api.yaml
  fi
  echo $env"_INTRA with GCP AWS"="`cat $env/$apiUpper/$doublon"_"$api.log|grep "and "$env"_INTRA"|wc -l`"

  if [ -e $env/$apiUpper/$env"_AWS"/$api/$api.yaml ]
  then
    for i in `cat $env/$apiUpper/doublon_p1_uniq.tmp`
      do
      if [[ -n $i ]]
      then
       sed -i "s/^\- $i/##\-$doublon"_aws" $i/g" $env/$apiUpper/$env"_AWS"/$api/$api.yaml
     fi
    done
 fi
  echo $env"_AWS with GCP"="`cat $env/$apiUpper/$doublon"_"$api.log|grep "and "$env"_AWS"|wc -l`"
  echo
done

rm -f $env/$apiUpper/doublon*.tmp

for TENANT in AZR AWS INTRA
do
   Tenant=${TENANT,,}
   #echo $TENANT, $tenant
  if [ -e $env/$apiUpper/$env"_"$TENANT/$api/$api.yaml ];then
   #echo "sed -i "s/##\-$doublon"_"$Tenant name:/\- name:/g" $env/$apiUpper/$env"_"$TENANT/$api/$api.yaml"
   sed -i "s/##\-differ_$Tenant name:/\- name:/g" $env/$apiUpper/$env"_"$TENANT/$api/$api.yaml 
   sed -i "s/##\-identical_$Tenant name:/\- name:/g" $env/$apiUpper/$env"_"$TENANT/$api/$api.yaml
   #export val$tenant=`cat $env/$apiUpper/$env"_"$tenant/$api/$api.yaml | grep "#-differ" | wc -l`
  fi
done

#val=$((valAZR+valAWS+valINTRA))
#echo DOUBLON_$apiUpper=$val
