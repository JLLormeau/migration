#!/bin/bash
. env.sh

echo $env
apiUpper=$1
api="${apiUpper,,}"

list=`grep -rl  \"key\":  ./$env/AZURE-CREDENTIALS |  grep "json"$`

echo $list
    
if [ ${#list} -ne  0 ]
then
   for file in $list
   do
   echo $file
   sed -i 's/\"key\": null/\"key\": \"xx\"/g' $file
   done
fi
