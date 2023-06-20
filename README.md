# InsTag
這是一個 `Python` 爬蟲。
輸入**關鍵字**，即可開始下載符合該**關鍵字**的 **Hashtag** 且為**公開貼文**的**圖片**。(預設儲存路徑為 `/save/<Hashtag>/`)

# Version
> Version：`v1.1`

> Last Update：`2023/06/31`

> Python：`v3.6.9`

# Step
1. Clone the project
```bash
$ git clone https://github.com/alpaca0x0/InsTag.git
$ cd InsTag/
```

2. Install libraries
```bash
$ pip3 install -r requirements.txt
```

3. Run it !
```bash
$ python main.py
```

# Usage

1. Run the `main.py`.
2. Enter a `#hashtag` for the image you want to download.
3. Check images. (By default the file will be saved to path `./save/<hashtag>/`)

### Arguments

> --auto, -a\
  No need to wait for seconds between pages. (頁數之間不須等待秒數，立刻開始下載下一頁)

> --debug, -d\
  Debug Mode (除錯模式，能夠顯示更多詳細資訊)

