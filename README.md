# InsTag
這是一個 `Python` 爬蟲。
輸入**關鍵字**，即可開始下載符合該**關鍵字**的**Hashtag**且為**公開貼文**的**圖片**。(預設儲存路徑為 `/save/<Hashtag>/`)

# Step
1. 安裝所需函式庫
```bash
$ pip3 install -r requirements
```

2. Git Clone
```bash
$ mkdir InsTag
$ cd InsTag/
$ git clone https://github.com/alpaca0x0/InsTag.git
```

3. Run!
```bash
$ python3 main.py
```

# 操作
打上關鍵字即可開始下載圖片。

# 相關參數
 > 自動跳過下載時，下一頁的等待秒數
 > ```bash
 > $ python3 main.py --auto
 > ```
 > or
 > ```bash
 > $ python3 main.py -a
 > ```

---

 > 除錯模式。可以看見詳細的後台運作步驟
 > ```bash
 > $ python3 main.py --debug
 > ```
 > or
 > ```bash
 > $ python3 main.py -d
 > ```
