#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

metricname=$1
dim=$2
dim2=${dim/:/=}
export MyTenant=$JLLTenant
export MyToken=$JLLToken
#export MyTenant=$env"Tenant"
#export MyTenant=$env"Token"


export URL_DT="https://"$MyTenant"/api/v2/metrics/ingest"
echo $URL_DT
export Header="Content-Type: text/plain; charset=utf-8"
export Metric=$metricname","$dim2" 0"
curl -H "Authorization: Api-Token "$MyToken"" -X POST -H "$Header" --data-ascii "$Metric" "$URL_DT"
