#!/bin/bash
workdir=$(cd `dirname $0`;pwd)
source ~/.bashrc
source activate py35

if [ -z $2 ]
then
    crawl_type="music"
else
    crawl_type=$2
fi

if [ -z $3 ]
then
    datetime=`date +"%Y%m%d%H"`
else
    datetime=$3
fi

if [ -z $1 ]
then
    freqType="hourly"
else
    freqType=$1
fi

if [ $crawl_type = "music" ] 
then
    echo "music"
    echo "python $workdir/crawl_bugs.py ${datetime} $freqType"
    /home/laesunk/anaconda2/envs/py35/bin/python $workdir/crawl_bugs.py ${datetime} $freqType >> $workdir/logs/bugs_${datetime}.log 2>&1
    echo "python /home/laesunk/anaconda2/envs/py35/bin/python $workdir/crawl_genie.py ${datetime} $freqType"
    /home/laesunk/anaconda2/envs/py35/bin/python $workdir/crawl_genie.py ${datetime} $freqType >> $workdir/logs/genie_${datetime}.log 2>&1
else
    echo "youtube"
    echo "/home/laesunk/anaconda2/envs/py35/bin/python $workdir/crawl_youtube.py ${datetime:0:8}"
    /home/laesunk/anaconda2/envs/py35/bin/python $workdir/crawl_youtube.py ${datetime:0:8} >> $workdir/logs/youtube_${datetime:0:8}.log
fi


