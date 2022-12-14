#!/bin/bash
. env.sh

echo $env

for mapp  in `cat $env"_MAPP/owner_mapping".csv`
do
    userid=`echo  $mapp | cut -d ";" -f 1`
    
    if [[ "$userid" != *"@"* ]]
    then
     #echo $userid
     alldash=`grep -rl -- \"$userid\" ./$api_saas | grep json$`
      if [ ${#alldash} -ne  0 ]
       then
        email=`echo  $mapp | cut -d ";" -f 2`
      
        for filetomap in $alldash
          do
           echo "Mapping "$userid" "$email"  "$filetomap 
           #echo "sed -i 's/\"$userid\"/\"$email\"/g' $filetomap"
           sed -i "s/\"$userid\"/\"$email\"/g" $filetomap
           done
        fi
      fi
done

