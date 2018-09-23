#!/bin/bash

workdir=$(cd `dirname $0`;pwd)
for date in `${BASE_PATH}/seqdate.py $startdate $enddate`
do
    $workdir/run.sh hourly ${date}
    
done
