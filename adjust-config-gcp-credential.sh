#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

apiUpper=$1
api="${apiUpper,,}"

list=`grep -rl  \"authToken\":  ./$env/KUBERNETES-CREDENTIALS |  grep "json"$`

echo $list
    
i=0
if [ ${#list} -ne  0 ]
then
   for file in $list
   do
   echo $file
   i=$((i+1))  
   echo $i
   url="https://tobedefinde_"$i
   echo $url
   sed -i 's/\"authToken\": null/\"authToken\": \"xx\"/g' $file
   sed -i 's/\"endpointUrl\": null/\"endpointUrl\": \"https:\/\/urltochange\"/g' $file
   sed -i "s/urltochange/urltochange_"$i"/" $file
   done
fi
