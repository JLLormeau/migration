#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

dashlog=$1
echo dashlog=$1
result=log/$env/result-dahboard-constraint-violation

cat $dashlog | grep Aggregation | sort | uniq > $result

sed -i 's/Aggregation/#/g' $result
sed -i 's/not supported/#/g' $result
sed -i 's/only supports/#/g' $result
sed -i 's/metric key/#/g' $result
sed -i 's/responsible config/#/g' $result

line=`cat $result | grep -n "#" | cut -d ":" -f 1 `

for dash in $line
do 
 echo $dash
 # sed -n $dash"p" $result | cut -d "#" -f 1
  echo "not supported => "  `sed -n $dash"p" $result | cut -d "#" -f 2  | cut -d \' -f 2`
  echo "metric : " `sed -n $dash"p" $result | cut -d "#" -f 3  | cut -d \' -f 2`
  echo "only supports : " ` sed -n $dash"p" $result | cut -d "#" -f 4  | cut -d \" -f 1 | cut -d " " -f2`
  echo "file : " `sed -n $dash"p" $result | cut -d "#" -f 5  | cut -d ":" -f 2 | cut -d " " -f2`
done
