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

    chartInfos = {}
    for page in range(1,5):
        if freqType=="hourly":
            date = inputDateTime[:-2]
            hour = inputDateTime[-2:]
            params = {'ymd':date, 'hh':hour, 'pg':str(page)}
            url = "http://www.genie.co.kr/chart/top200?ditc=D&rtm=Y&"
            targetSector = "list-wrap"
        elif freqType=="daily":
            date = inputDateTime[:-2]
            params = {'ymd':date, 'pg':str(page)}
            url = "http://www.genie.co.kr/chart/top200?ditc=D&rtm=N&"
            targetSector = "list-wrap"
        reqUrl = url+urllib.parse.urlencode(params)
        siteTxt = urllib.request.urlopen(reqUrl).read()
        soup =  BeautifulSoup(siteTxt, "html.parser" )
        for i in soup.select("."+targetSector+" tbody tr"):
            title = i.select(".info .title")[0].get_text().strip()
            chartInfos.setdefault(title,{})
            chartInfos[title]['artist'] = i.select(".info .artist")[0].get_text().strip()
            chartInfos[title]['songId'] = i['songid']
            chartInfos[title]['albumTitle'] = i.select(".info .albumtitle")[0].get_text().strip()
            chartInfos[title]['ranking'] = i.select(".number")[0].get_text().split(" ")[0].strip()

    return chartInfos 

if __name__=="__main__":
    if len(sys.argv)<1:
        print("input date, hour need")
        sys.exit(1)

    inputDateTime = sys.argv[1]
    freqType = sys.argv[2]

    top100List = getData(freqType,inputDateTime)

    with open("/home/ubuntu/song_index/data/music/genie_"+inputDateTime+"_"+freqType+".txt",'w',encoding='utf8') as f:
        for title in top100List:
            f.write("%s\t%s\t%s\t%s\t%s\n" %(top100List[title]['albumTitle'],top100List[title]['artist'],top100List[title]['songId'],title,top100List[title]['ranking']))
