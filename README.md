# InsTag
這是一個 `Python` 爬蟲。
輸入**關鍵字**，即可開始下載符合該**關鍵字**的**Hashtag**且為**公開貼文**的**圖片**。(預設儲存路徑為 `/save/<Hashtag>/`)

# Version
測試版本為 **Python 3.6.9**
(其他版本請自行測試，建議至少 **Python 3**)

# Step
1. 安裝所需函式庫
```bash
$ pip3 install -r requirements.txt
```

2. Git Clone
```bash
$ git clone https://github.com/alpaca0x0/InsTag.git
$ cd InsTag/
```

3. Run!
```bash
$ python main.py
```

# 操作
打上關鍵字即可開始下載圖片。

# 相關參數
 > 自動跳過在下載時存在下一頁的等待秒數
 > ```bash
 > $ python main.py --auto
 > ```
 > or
 > ```bash
 > $ python main.py -a
 > ```

---

 > 除錯模式。可以看見較為詳細的後台運作
 > ```bash
 > $ python main.py --debug
 > ```
 > or
 > ```bash
 > $ python main.py -d
 > ```
