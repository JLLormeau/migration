#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh


entity=`ls "$env"_"$tenant"_MAPP/entity_*_mapping.csv` 
#echo $entity

for api in $entity
do
  echo $api
 
 if [ `cat $api | wc -l`  -gt 0 ]
 then
  sed -i "s/ /_/g" $api
  for mapp  in `cat $api`
  do
    id_managed=`echo  $mapp | cut -d ";" -f 1` 
    echo $id_managed
    allfiles=`grep -rl -- $id_managed ./$local_rep | grep json$`
    if [ ${#allfiles} -ne  0 ]
      then
       id_saas=`echo  $mapp | cut -d ";" -f 2`
       entityname=`echo $mapp | cut -d ";" -f 3`
        for filetomap in $allfiles
         do
          echo "Mapping" $api"; entity "$entityname" : "$id_managed" ==> "$id_saas" for "$filetomap 
          #echo "sed -i "s/$id_managed/$id_saas/g" "$filetomap""
          sed -i "s/$id_managed/$id_saas/g" $filetomap
         done
      fi
   done
 fi
done
