#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

apiUpper=$1
api="${apiUpper,,}"

list=`grep -rl -- ^" \"order\":" ./$env/SERVICE-DETECTION-OPAQUE-WEB-REQUEST | grep "json"$`
    
if [ ${#list} -ne  0 ]
then
   for file in $list
   do
   linetodelete=`cat  $file | grep -n ^" \"order\":" | cut -d ":" -f 1`
   if [ ${#linetodelete} -ne  0 ]
   then
    echo $file
    cat  $file | grep -n ^"   \"id\":"
    param=$linetodelete"d"
    echo "clean line "$param
    sed $param $file > $file.2
    mv $file.2 $file
   fi
   done
fi
