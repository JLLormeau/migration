#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

echo "#ALL" > ALL
mkdir -p log/$env
export directory=Deploy-$env-source
#export directory=Deploy-$env-calc
echo directory_source=$directory
echo directory_target=$env
managed_tenant=`ls ./$directory/*`
echo > list_api
for entry in $managed_tenant
 do
   echo "$entry" >> list_api
done
api=`cat list_api | sort | uniq | grep -E -v / `
echo "==> ./step_deploy.sh ALL"
for entry2 in  $api
do
 entryUpper="${entry2^^}"
 if [ `echo $entryUpper |wc -c` -gt 1  ]
 then
   if  [ $entryUpper != APPLICATION  ] && [ $entryUpper != KUBERNETES-CREDENTIALS ]
   then
    echo $entryUpper
    echo $entryUpper >> ALL
   fi
 fi
 for i in GCP AWS AZR INTRA
 do
   #entryUpper="${entry2^^}"
   mkdir -p $env/$entryUpper/$env"_"$i/$entry2
   cp -r  $directory/$env"_"$i/$entry2/* $env/$entryUpper/$env"_"$i/$entry2 2> /dev/null
   cp -r  $directory/$i/$entry2/* $env/$entryUpper/$env"_"$i/$entry2 2> /dev/null
 done
done
