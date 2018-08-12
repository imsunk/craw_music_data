# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import sys

def getData(freqType,inputDateTime):
    url=""
    hour=""
    params=""
    date=""
    targetSector=""
    if freqType=="hourly":
        date = inputDateTime[:-2]
        hour = inputDateTime[-2:]
        params = {'charthour':hour, 'chartdate':date}
        url = "https://music.bugs.co.kr/chart/track/realtime/total?"
        targetSector = "CHARTrealtime"
    elif freqType=="daily":
        date = inputDateTime[:-2]
        params = {'chartdate':date}
        url = "https://music.bugs.co.kr/chart/track/day/total?"
        targetSector = "CHARTday"
    reqUrl = url+urllib.parse.urlencode(params)
    siteTxt = urllib.request.urlopen(reqUrl).read()
    soup =  BeautifulSoup(siteTxt, "html.parser" )

    hourlyChartInfos = {}
    for i in soup.select("#"+targetSector+" tbody tr"):
        title = i.select(".title a")[0].get_text()
        hourlyChartInfos.setdefault(title,{})
        hourlyChartInfos[title]['albumId'] = i['albumid']
        hourlyChartInfos[title]['artistId'] = i['artistid']
        hourlyChartInfos[title]['trackId'] = i['trackid']
        hourlyChartInfos[title]['artist'] = i.select(".artist a")[0].get_text()
        hourlyChartInfos[title]['ranking'] = i.select(".ranking strong")[0].get_text()

    return hourlyChartInfos 

if __name__=="__main__":
    if len(sys.argv)<1:
        print("input date, hour need")
        sys.exit(1)

    inputDateTime = sys.argv[1]
    freqType = sys.argv[2]

    top100List = getData(freqType,inputDateTime)

    with open("/home/ubuntu/song_index/data/music/bugs_"+inputDateTime+"_"+freqType+".txt",'w',encoding='utf8') as f:
        for title in top100List:
            f.write("%s\t%s\t%s\t%s\t%s\t%s\n" %(top100List[title]['albumId'],top100List[title]['artistId'],top100List[title]['trackId'],top100List[title]['artist'],title,top100List[title]['ranking']))
