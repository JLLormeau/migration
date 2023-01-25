#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

#echo $1
for i in 025da242-3c4b-3449-bfc3-85401a20a5b3 46930001-6b5c-3c41-95a3-4f234c848bda 62f69a81-10e0-3b29-ae95-f73122d55b91 0bbab193-5bcc-3f13-9a32-3331d011f90c 8de158c5-3137-33fc-a221-10d890910b33 bd288dbe-34a8-3914-8f6b-68f940552925 cd205cb1-a748-3597-b365-eb0be86e06c6 fc4e9518-9472-35c5-933b-f96bf55eae8b 53b1f6cf-ec7c-3d5a-a3e0-d2b71492358d 0b5792e2-4ea5-3819-8aa2-0e1160511e5b fa7854a1-5d56-39d1-ab75-984e8c1fb374 37861f93-1a9d-3ef7-8173-c34f7cdd8c5c 7493aa26-cf9d-3f8b-a207-bbf16179db7c 158fa28f-1551-3794-a4e1-7b467befe273 ecea9fc2-5a7c-3706-ada1-6e819e2f1d2a bd112aad-cad7-3bcf-9742-ab3c587dc6e8 f2b1539f-05a9-3458-be73-c88214128e8d 977a3dd8-a597-3d37-8dc0-4104088ec021 972ac82e-d0e7-326d-90df-0820cb40139a d6b909eb-87ef-3d95-bf9a-36c6434f422c b1aebeec-6165-35e1-bee6-a16301650d1f 2d0bae18-d336-30de-a605-0f57947504c8 f78fb437-fd0c-3674-9724-0a1f2e234e8f 761de6e6-593a-376c-aeb4-c105de35697e 53d4b5f4-e4b5-308c-8e33-b52854d4db12 c8cdad50-bfbd-3a4c-9896-8d584062b879 38fe4521-4f8e-39a2-b0b7-f79f1b7c6c7a cd291e3d-31aa-3cd3-ab5e-ddc5a0483fe0 35168c9e-9450-3e8a-8255-a262afad15bc 49595e98-9f40-3cef-81be-946f88b7b4a2 d9687ca8-a6a0-32eb-83aa-db18263b4343 c45d8620-d69d-39eb-ba32-b3e2d83235a2
do
  json=`find ./$env/* -name  $i.json`
  APP_ID=`cat $json | grep APP | cut -d ":" -f 2 | cut -d "\"" -f 2 `
  APP_NAME=`cat "$env"_MAPP/APP_WEB_id_source.csv  | grep $APP_ID | cut -d ";" -f 2`
  echo $i, $APP_NAME
done
