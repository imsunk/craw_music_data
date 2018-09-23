# coding= utf-8

from bs4 import BeautifulSoup
from urllib.request import urlopen
import urllib.parse
import pickle
import sys
import urllib3
urllib3.disable_warnings()
import json
import time
import os.path
import logging
import logging.config
#sys.setdefaultencoding("utf-8")

def getApiKeyIdx(apiKeys,number,idx):
    if idx>int(number/500):
        return idx
    else:
        return int(number/500)

def nextApiKey(apiKeys, idx):
    return idx+1,apiKeys[idx+1]

def getLogger():
    with open("/home/laesunk/song_index/logger.json") as f:
        config_dict = json.load(f)
    logging.config.dictConfig(config_dict)
    logger = logging.getLogger(__name__)

    return logger

def getBjList():
    url = """https://socialerus.com/jsonData/ranking_list_json.asp?gotoPage=1&v_seq=&schRankDT=&schRankStart=&schRankEnd=&schCategory=&schType=&schText=&pb_orderBy=&pb_orderByOptlon=DESC&pageSize=3000"""
    bjList=urllib.request.urlopen(url).read()
    streamList = json.loads(bjList.decode("utf-8"))

    youtubeInfo = {}
    youtubeInfo["infos"] = []
    for s in streamList["list"]:
        info = {}
        info["channelName"] = s["CCD_TITLE"]
        info["channelId"] = s["C_CHANNELID"]
        info["channelUrl"] = "https://www.youtube.com/channel/%s" %(s["C_CHANNELID"])
        info["category"] = s["CCD_CATEGORY_NAME"]
        info["videoInfos"] = []
        info["channelStatistics"] = {}
        info["profileImg"] = ""
        info["startDate"] = ""
        youtubeInfo["infos"].append(info)
    return youtubeInfo

if __name__=="__main__":
    logger = getLogger()
    logger.info("crawl_start")
    inputDateTime = sys.argv[1]

    getCnt=50
    allVideos = {'infos':[]}

    apiKeys = ["AIzaSyCPHgo1r-oIJ8kKoI0ReGkRof-LWyLbnH4","AIzaSyCVbRoYTWteAtR-QBYj8pfgsTkGmKQQ8A4",
    "AIzaSyB6WcnlDRh-1Y7QI7gjPrnyUhznrujpcRE","AIzaSyAUsTcrkRuSlJXw9tRQ2GfHuVt2am2iedI","AIzaSyC_MrfTbOsFjYBQ3C9BqeB2Cp5M4o2GSOs","AIzaSyCPXOWhaI70F6j1MlKmEUo_0-tNlFDcuuI"]
    output =  open("/home/laesunk/song_index/data/youtube/youtube_"+inputDateTime+".txt",'w',encoding='utf8')
    http = urllib3.PoolManager()
    youtubeInfo = None

    if os.path.isfile("/home/laesunk/song_index/youtubeList.pickle"):
        with open('/home/laesunk/song_index/youtubeList.pickle', 'rb') as handle:
            youtubeInfo = pickle.load(handle)
    else:
        youtubeInfo = getBjList()
        with open('/home/laesunk/song_index/youtubeList.pickle', 'wb') as handle:
            pickle.dump(youtubeInfo, handle, protocol=pickle.HIGHEST_PROTOCOL)
        
    idx=0
    for i, tuber in enumerate(youtubeInfo['infos']):
        idx = getApiKeyIdx(apiKeys,i,idx)
        apiKey = apiKeys[idx]
#logger.info("apikey : "+apiKey)
        vidList = []
        channelInfoUrl = "https://www.googleapis.com/youtube/v3/channels?key=%s&part=id,snippet,statistics&id=%s" %(apiKey,tuber['channelId'])
        channelInfo = http.request('GET', channelInfoUrl)
        channelInfo = json.loads(channelInfo.data.decode("utf-8"))

        if channelInfo.get('items')==None:
            idx,apiKey = nextApiKey(apiKeys,idx)
            channelInfoUrl = "https://www.googleapis.com/youtube/v3/channels?key=%s&part=id,snippet,statistics&id=%s" %(apiKey,tuber['channelId'])
            channelInfo = http.request('GET', channelInfoUrl)
            channelInfo = json.loads(channelInfo.data.decode("utf-8"))

        '''
        tuber['channelStatistics'] = channelInfo['items'][0]['statistics']
        tuber['profileImg'] = channelInfo['items'][0]["snippet"]['thumbnails']['high']['url']
        tuber['startDate'] = channelInfo['items'][0]["snippet"]['publishedAt']
        '''
        try:
            if int(channelInfo['items'][0]['statistics']['viewCount'])<10000:
                continue
        except:
            continue
        videoData={}
        videoData['channelStatistics'] = channelInfo['items'][0]['statistics'] if channelInfo['items'][0].get("statistics")!=None else ""
        videoData['profileImg'] = channelInfo['items'][0]["snippet"]['thumbnails']['high']['url'] if len(channelInfo['items'][0]["snippet"]['thumbnails'])!=0 else ""
        videoData['startDate'] = channelInfo['items'][0]["snippet"]['publishedAt']
        videoData['videoInfos'] = []
        videoData["channelName"] = tuber["channelName"]
        videoData["channelId"] = tuber["channelId"]
        videoData["channelUrl"] = tuber["channelUrl"]
        videoData["category"] = tuber["category"]
        
        post_params = {
            'pageToken' : "",
            'maxResults': 50,
            'channelId': tuber['channelId']
        }
        
        chIdUrl = "https://www.googleapis.com/youtube/v3/search?key=%s&part=snippet,id&order=date" %(apiKey)
        while(1):
            encoded = urllib.parse.urlencode(post_params)
            result = http.request('GET', chIdUrl+"&"+encoded)
            videoList = json.loads(result.data.decode("utf-8"))
            if videoList.get("items")==None:
                idx,apiKey = nextApiKey(apiKeys,idx)
                chIdUrl = "https://www.googleapis.com/youtube/v3/search?key=%s&part=snippet,id&order=date" %(apiKey)
                result = http.request('GET', chIdUrl+"&"+encoded)
                videoList = json.loads(result.data.decode("utf-8"))

            #print(videoList['pageInfo']['totalResults'])
            if (videoList.get("nextPageToken")==None) and len(videoList['items'])==0:
                break
            
            for v in videoList["items"]:
                if v['id'].get('videoId')==None:
                    continue
                vidList.append(v['id']['videoId'])
                
            if videoList.get("nextPageToken")!=None:
                pageToken = videoList["nextPageToken"]
                post_params['pageToken'] = pageToken
            
            if (videoList.get("nextPageToken")==None) and len(videoList['items'])!=0:
                break

        reqCnt = int(len(vidList)/getCnt)+1
        for s in range(0,reqCnt):
            st = s*50
            ed = (s+1)*50
            vids = ",".join(vidList[st:ed])
            tUrl = "https://www.googleapis.com/youtube/v3/videos?id=%s&part=snippet,statistics&key=%s&order=date"%(vids,apiKey) 
            stats=urllib.request.urlopen(tUrl).read()
            statInfos = json.loads(stats.decode("utf-8"))
            if statInfos.get("items")==None:
                idx,apiKey = nextApiKey(apiKeys,idx)
                tUrl = "https://www.googleapis.com/youtube/v3/videos?id=%s&part=snippet,statistics&key=%s&order=date"%(vids,apiKey) 
                stats=urllib.request.urlopen(tUrl).read()
                statInfos = json.loads(stats.decode("utf-8"))

            if len(statInfos.get("items"))==0:
                logger.info("no stat/"+tuber["channelId"]+"/"+tuber['channelName'])
                continue

            for stat in statInfos['items']:
                statInfos = {}
                try:
                    statInfos['vid'] = stat['id']
                    statInfos['videoDate'] = stat['snippet']["publishedAt"]
                    statInfos['title'] = stat['snippet']["title"]
                    statInfos['thumbnail'] = stat['snippet']["thumbnails"]['high']['url']
                    statInfos['live'] = stat['snippet']['liveBroadcastContent']
                    statInfos['statistics'] = stat['statistics']
                except Exception as ex:
                    logger.info("video info parsing error / "+ tuber['channelId']+"/"+stat['id']+"/"+ ex)
                #print (statInfos)
                videoData['videoInfos'].append(statInfos)

        allVideos['infos'].append(videoData)
           #print(tuber['channelName']+" reading")

        if i%10==0:
            print (i)
            for video in allVideos['infos']:
                output.write(json.dumps(video)+"\n")
            allVideos = {'infos':[]}
        time.sleep(0.5)
        logger.info(str(i)+"/"+tuber['channelName']+"/"+tuber["channelId"]+" done")

    if len(allVideos['infos'])!=0:
        for video in allVideos['infos']:
            output.write(json.dumps(video)+"\n")
            #print(video['channelName']+" has been recored")
    logger.info("crawl_end")
    output.close()
