#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

for mapp  in `cat $env"_MAPP/bf_mapping".csv`
do
    url=`echo  $mapp | cut -d ";" -f 1`
    
     echo $url
     alldash=`grep -rl -- $url ./$local_rep | grep json$`
     #echo "grep -rl -- \"$url\" ./$local_rep | grep json$"
     #echo $alldash
     
      if [ ${#alldash} -ne  0 ]
       then
        newurl=`echo  $mapp | cut -d ";" -f 2`
        #echo $newurl
        #echo $alldash
      
        for filetomap in $alldash
          do
           echo "Mapping "$url" "$newurl"  "$filetomap 
           echo "sed -i 's#$url#$newurl#g' $filetomap"
           sed -i "s#$url#$newurl#g" $filetomap
           done
        fi
done

