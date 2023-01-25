#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

for api  in MZ APP_WEB APP_MOBILE RequestAttribute SLO SYNTH SYNTH_LOCATION Dashboards AlertingProfile
do
  sed -i "s/ /_/g" $env"_MAPP"/$api"_mapping".csv
  for mapp  in `cat $env"_MAPP"/$api"_mapping".csv`
  do
    id_managed=`echo  $mapp | cut -d ";" -f 1` 
    allfiles=`grep -rl -- $id_managed ./$env/ | grep json$`
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
done
