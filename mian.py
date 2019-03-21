import requests
import math
import json
import time

website_url = 'https://github.red'

wordsTotal = 0

def GetPostTotal():
    req = requests.get(website_url + '/wp-json/wp/v2/posts?context=view&per_page=1&page=1')
    return int(req.headers['X-WP-Total'])

def CalChineseWord(str):
    count = 0
    for s in str:
        if '\u4e00' <= s <= '\u9fff':
            count += 1

    return count


def FormatTime(timeStr):
    return str(time.strftime("%Y年%m月%d日", time.localtime(math.ceil(time.mktime(time.strptime(timeStr, "%Y-%m-%dT%H:%M:%S"))))))

def CalculateWord():
    perPage = 50
    postTotal = GetPostTotal()
    totalPage = math.ceil(postTotal / perPage)

    wordsCount = 0

    for nowPage in range(1, totalPage + 1):
        pageReq = requests.get(website_url + '/wp-json/wp/v2/posts?context=view&per_page=' + str(perPage) + '&page=' + str(nowPage))
        postData = json.loads(pageReq.text)
        dataCount = len(postData)

        print("正在统计第 " + str(nowPage) + " 页，共 " + str(dataCount) + " 篇文章。")

        for nowPost in range(0, dataCount):
            title = postData[nowPost]['title']['rendered']
            content = postData[nowPost]['content']['rendered']
            count = CalChineseWord(content)

            print(title + "（" + str(count) + "字） " + FormatTime(postData[nowPost]['date']))

            wordsCount += count

    return wordsCount


def GetFirstPost():
    req = requests.get(website_url + '/wp-json/wp/v2/posts?context=view&per_page=1&page=1&order=asc')
    content = json.loads(req.text)

    return [time.localtime(math.ceil(time.mktime(time.strptime(content[0]['date'], "%Y-%m-%dT%H:%M:%S")))), content[0]['title']['rendered']]

allWord = str(CalculateWord())
allPost = str(GetPostTotal())
print("\n" + website_url)
print("第一篇文章发表于" + str(time.strftime("%Y年%m月%d日", GetFirstPost()[0])) + "。")
print("总共 " + allPost +" 篇文章，共 "+ allWord + " 个中文字符。")