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
	if not len(glob.glob(save_path+file_name+"*"))>0:
		os.mknod(save_path+file_name)
	else:
		print("檔案已存在，跳過「"+save_path+file_name+"」\n")
		return

	data_download=requests.get(file_url,headers=req_headers,stream=True,timeout=15)
	# save
	bar_size=30 #loading bar 寬度
	size=0 #檔案已下載的大小
	chunk_size = 1024 #每次所讀取的大小
	total_size = int(data_download.headers['content-length']) #檔案總大小
	start=time.time()
	
	with open(save_path+file_name,"wb") as f:
		for data in data_download.iter_content(chunk_size=chunk_size):
			if data:
				f.write(data)
			size += len(data)
			now = time.time()
			sys.stdout.write('\r'+"進度: "+u"\u250b"+int(size/total_size*bar_size)*u"\u2588"+int(bar_size-(size/total_size*bar_size))*" "+u"\u250b"+"【"+str("%.02f"%round(size/chunk_size/1024,2))+"/"+str("%.02f"%round(float(total_size/chunk_size/1024),2))+" MB】"+"【"+str("%.02f"%round(float(size/total_size)*100,2))+"%"+"】【"+time_str(days="d ",hours="h ",minutes="m ",seconds="s",t_sec=int(now-start))+"】")
			sys.stdout.flush()
	end = time.time()

	kind = filetype.guess(save_path+file_name)
	#print('\nFile MIME type: '+str(kind.mime))
	os.rename(save_path+file_name,save_path+file_name+"."+kind.extension)
	print("Saved!\n")
