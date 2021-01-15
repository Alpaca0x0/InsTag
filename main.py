# -*- coding: utf-8 -*
import sys
from datetime import datetime
import requests #請求
from bs4 import BeautifulSoup as soup #解析html
from fake_useragent import UserAgent #偽裝請求
import modules #sys.path.append("modules")
import json #解析 json
import signal #signal 判斷ctrl+c
import time #Sleep
import download #引入下載功能

#############################################

class _info():
    def __init__(self):
        self.name="Instag"
        self.author="Alpaca0x0"
        self.version="1.0"
        self.update="2021/01/16"
_info=_info()

#############################################

sysDebug=False #debug
sysAuto=False #auto download
if ("--help" in sys.argv) or ("-h" in sys.argv):
    print("Commands:")
    print("  --auto, -a\n  No need to wait for seconds between pages. (頁數之間不須等待秒數，立刻開始下載下一頁)。\n")
    print("  --debug, -d\n  Debug Mode. (除錯模式)\n")

    exit()

if ("--auto" in sys.argv) or ("-a" in sys.argv):
    sysAuto=True;
    print("Auto Mode On")
if ("--debug" in sys.argv) or ("-d" in sys.argv):
    sysDebug=True;
    print("Debug Mode On")

#############################################

def exit(signum, frame):
    print('\n Stoped '+_info.name+'！ \n')
    sys.exit()
signal.signal(signal.SIGINT, exit)
signal.signal(signal.SIGTERM, exit)

def interrupted(signum, frame):
    raise InputTimeoutError

def set_header_user_agent():
    user_agent = UserAgent()
    return user_agent.random

#############################################

class Req:
  def __init__(self, protocol, domain, path, keyword, hasNext=""):
    self.protocol=protocol
    self.domain=domain
    self.path=path
    self.keyword=keyword
    self.hasNext=hasNext

    self.url=self.protocol+self.domain+self.path+self.keyword+self.hasNext

    self.p=requests.Session()
    self.useragent=set_header_user_agent()
    self.headers={"User-Agent": self.useragent}
    self.data=""

#############################################
print(" ___           _              \n|_ _|_ __  ___| |_ __ _  __ _ \n | || '_ \/ __| __/ _` |/ _` |\n | || | | \__ \ || (_| | (_| |\n|___|_| |_|___/\__\__,_|\__, |\n                        |___/")
#############################################
print("《Version》"+_info.name+" "+_info.version)
print("《Author》"+_info.author)
print("\nHelp? Run with \"--help\".")

# 請求＆回應
while 1:
    print("-"*32)
    jump=False #break double loop    
    keyword=input("關鍵字：＃").strip().replace(" ","")
    while keyword=="":
        keyword=input("請輸入關鍵字：＃").strip().replace(" ","")
        continue
    while 1:
        req=Req("https://","imginn.com","/api/tags/?id=",keyword) #目標
        req.data=requests.get(req.url,headers=req.headers,timeout=15) #將此頁面的HTML GET下來
        print("Host -> "+req.domain+" -> "+str(req.data.status_code))
        if req.data.status_code != requests.codes.ok:
            print("Bad request -「"+req.url+"」\n")
            if sysAuto:
                print("-"*32)
                print("關鍵字：＃"+req.keyword)
                continue
            else:
                if input("請求失敗，繼續？ (Y/N) ").lower().strip() == "n":
                    jump=True #break double loop    
                    break
                else:
                    print("-"*32)
                    print("關鍵字：＃"+req.keyword)
                    continue
        else:
            break
    if jump:
        continue


# 解析
    download_part=1
    jump="n"
    while 1:
        req.data.encoding="utf-8"
        req.data=req.data.text
        datas=json.loads(req.data)

#下載
        for i in range(len(datas["items"])):
            req.useragent=set_header_user_agent()
            req.headers={"User-Agent": req.useragent}
            download.download(req_headers=req.headers,file_name=datas["items"][i]["code"]+"_"+datas["items"][i]["alt"],file_url=datas["items"][i]["src"],save_path="./save/"+req.keyword+"/")

    #存在下一頁
        if datas["hasNext"]:
            if not sysAuto:
                signal.signal(signal.SIGALRM, interrupted)
                signal.alarm(5) #計時5秒
                try:
                    jump=input("存在下一頁，繼續下載嗎 (5秒後 自動下載)？ (Y/N) ").lower().strip()
                except: #InputTimeoutError:
                    #無訊號，默認繼續下載
                    print("繼續下載...")
                    jump="y"
                #class InputTimeoutError(Exception):
                signal.alarm(0)  # 讀到輸入信號，重置
                if jump == "n":
                    print("取消繼續")
                    break
            else:
                print("\n存在下一頁，接收參數「--auto」自動下載...")

            while 1:
                jump=False
                req=Req(req.protocol,req.domain,req.path,keyword=req.keyword,hasNext="&cursor="+datas["cursor"]) #目標
                req.data=requests.get(req.url,headers=req.headers,timeout=15) #將此頁面的HTML GET下來
                print("Host -> "+req.domain+" -> "+str(req.data.status_code))
                if req.data.status_code != requests.codes.ok:
                    print("Bad request -「"+req.url+"」\n")
                    if sysAuto:
                        print("關鍵字：#"+req.keyword+" (part."+str(download_part)+")")
                        continue
                    else:
                        if input("請求失敗，繼續？ (Y/N) ").lower().strip() == "n":
                            jump=True #break double loop    
                            break
                        else:
                            print("關鍵字：#"+req.keyword+" (part."+str(download_part)+")")
                            continue
                else:
                    download_part=download_part+1
                    break
            if jump:
                break
            else:
                continue
        else:
            print("爬蟲結束")
            break
