# -*- coding: utf-8 -*
import sys
import requests
import time
import os
import filetype #判斷檔案類型
import glob #萬用字元，比較檔名是否存在

def time_str(t_sec,days="day ",hours="hour ",minutes="min ",seconds="sec"):
	# t_sec is time sec(int)
	t_sec=int(t_sec)

	if int(t_sec/60)>0: # min >
		if int(t_sec/60/60)>0: # hour >
			if int(t_sec/60/60/24)>0: # day >
				return str(int(t_sec/60/60/24))+days+str(int(t_sec/60/60)).zfill(2)+hours+str(int(t_sec/60)).zfill(2)+minutes+str(int(t_sec%60)).zfill(2)+seconds
			else: # hour min sec
				return str(int(t_sec/60/60)).zfill(2)+hours+str(int(t_sec/60)).zfill(2)+minutes+str(int(t_sec%60)).zfill(2)+seconds
		else: # min sec
			return str(int(t_sec/60)).zfill(2)+minutes+str(int(t_sec%60)).zfill(2)+seconds
	else: # sec
		return str(int(t_sec%60)).zfill(2)+seconds

def download(req_headers,file_name,file_url,save_path=""):
	n_filename=["\"","/","\\","\n","\t","<",">",":","|","?","*","'",".","","　","(",")","，","。","！","？","＃"]
	file_name=file_name.strip() #去除頭尾空格
	for n_f in n_filename:
		file_name=file_name.replace(n_f,"")
	if len(file_name)>70:
		file_name=file_name[0:70]

	if not os.path.exists(save_path):
		os.makedirs(save_path)
	if len(glob.glob(save_path+file_name+".*"))>0:
		sys.stdout.write("\r檔案已存在，跳過「"+save_path+file_name+"」\n")
		sys.stdout.flush()
		sys.stdout.write("\u001b[1A\u001b[2K")
		return

	data_download=requests.get(file_url,headers=req_headers,stream=True,timeout=15)
	# save
	bar_size=20 #loading bar 寬度
	size=0 #檔案已下載的大小
	chunk_size = 1024 #每次所讀取的大小
	total_size = int(data_download.headers['content-length'] if 'content-length' in data_download.headers else data_download.headers['x-full-image-content-length']) #檔案總大小
	start = time.time() #開始下載的時間
	now = time.time() #當前時間
	got_size = 0 #當前遠端檔案已讀取大小
	
	with open(save_path+file_name,"wb") as f:
		got_size = 0
		for data in data_download.iter_content(chunk_size=chunk_size):
			got_size += len(data)
			size = f.seek(0, 2)
			if(got_size < size): continue #如果當前檔案大小比已抓取的遠端檔案大小大，則繼續抓取不重複寫入
			if data: f.write(data)
			now = time.time()
			sys.stdout.write("\u001b[2K"+"\r下載中 "+u"\u250b"+int(size/total_size*bar_size)*u"\u2588"+int(bar_size-(size/total_size*bar_size)+1)*" "+u"\u250b"+"【"+str("%.02f"%round(size/chunk_size/1024,2))+" / "+str("%.02f"%round(float(total_size/chunk_size),2))+" KB】"+"【"+str(int((size/total_size)*100))+"%"+"】【"+time_str(days="d ",hours="h ",minutes="m ",seconds="s",t_sec=int(now-start))+"】")
			sys.stdout.flush()
		sys.stdout.write("\u001b[2K"+"\r已下載 【"+str("%.02f"%round(float(f.seek(0, 2)/chunk_size),2))+" KB】【"+time_str(days="d ",hours="h ",minutes="m ",seconds="s",t_sec=int(now-start))+"】")
		sys.stdout.flush()
	
	end = time.time()

	kind = filetype.guess(save_path+file_name)
	#print('\nFile MIME type: '+str(kind.mime))
	os.rename(save_path+file_name,save_path+file_name+"."+kind.extension)

	print("- " + file_name+"."+kind.extension)
	sys.stdout.flush()
	