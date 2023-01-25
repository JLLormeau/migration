#!/bin/bash
echo "##"
echo script_name ${0##*/}
. env.sh

echo rabbitmq disable on "$env"/AUTO-TAG/"$env"_AZR/auto-tag/auto-tag.yaml - doublon with RabbotMQ
sed -i 's/^\- rabbitmq/##error\- rabbitmq/g' "$env"/AUTO-TAG/"$env"_AZR/auto-tag/auto-tag.yaml
cat "$env"/AUTO-TAG/"$env"_AZR/auto-tag/auto-tag.yaml | grep rabbitmq | grep error



echo metricsevents disable bug  when metricSelector is not yet created
echo on "$env"/ANOMALY-DETECTION-METRICS/"$env"_AZR/anomaly-detection-metrics/anomaly-detection-metrics.yaml
sed -i 's/^\- HighRabbitMQfiledescriptorsusage/##error\- HighRabbitMQfiledescriptorsusage/g' "$env"/ANOMALY-DETECTION-METRICS/"$env"_AZR/anomaly-detection-metrics/anomaly-detection-metrics.yaml
sed -i 's/^\- HighRabbitMQmemoryusage/##error\- HighRabbitMQmemoryusage/g' "$env"/ANOMALY-DETECTION-METRICS/"$env"_AZR/anomaly-detection-metrics/anomaly-detection-metrics.yaml
sed -i 's/^\- HighRabbitMQprocessesusage/##error\- HighRabbitMQprocessesusage/g' "$env"/ANOMALY-DETECTION-METRICS/"$env"_AZR/anomaly-detection-metrics/anomaly-detection-metrics.yaml
sed -i 's/^\- HighRabbitMQsocketsusage/##error\- HighRabbitMQsocketsusage/g' "$env"/ANOMALY-DETECTION-METRICS/"$env"_AZR/anomaly-detection-metrics/anomaly-detection-metrics.yaml
cat "$env"/ANOMALY-DETECTION-METRICS/"$env"_AZR/anomaly-detection-metrics/anomaly-detection-metrics.yaml | grep abbit | grep error


echo ANOMALY-DETECTION-DISKS disable dxi-DXISDB doublon with dwi-dxisdb on  "$env"/ANOMALY-DETECTION-DISKS/"$env"_INTRA/anomaly-detection-disks/anomaly-detection-disks.yaml
sed -i 's/^\- dxi-DXISDB/##error\- dxi-DXISDB/g'  "$env"/ANOMALY-DETECTION-DISKS/"$env"_INTRA/anomaly-detection-disks/anomaly-detection-disks.yaml
cat "$env"/ANOMALY-DETECTION-DISKS/"$env"_INTRA/anomaly-detection-disks/anomaly-detection-disks.yaml | grep dxi-DXISDB | grep error

