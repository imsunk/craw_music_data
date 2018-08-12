# coding= utf-8

import pickle
import sys
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
    with open("/home/ubuntu/song_index/logger.json") as f:
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
    logger.info("crawl_end")

    youtubeInfo = None
    if os.path.isfile("/home/ubuntu/song_index/youtubeList.pickle"):
        with open('/home/ubuntu/song_index/youtubeList.pickle', 'rb') as handle:
            youtubeInfo = pickle.load(handle)
    else:
        youtubeInfo = getBjList()
        with open('/home/ubuntu/song_index/youtubeList.pickle', 'wb') as handle:
            pickle.dump(youtubeInfo, handle, protocol=pickle.HIGHEST_PROTOCOL)

    out = open("/home/ubuntu/song_index/data/new_bj/bj_list.txt",'w',encoding="utf-8")

    for bj in youtubeInfo['infos']:
        out.write(bj['channelName']+""+bj['channelId']+"\n")
    out.close()
