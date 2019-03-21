import requests
import math
import json

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

            print(title + "（" + str(count) + "字）")

            wordsCount += count

    return wordsCount

def GetFirstPost():
    req = requests.get('https://github.red/wp-json/wp/v2/posts?context=view&per_page=1&page=1&order=asc')
    req = json.loads(req.text)

    return [req[0]['date'], req[0]['title']['rendered']]

allWord = str(CalculateWord())
allPost = str(GetPostTotal())
print("")
print(website_url)
print()
print("总共 " +  +" 篇文章，共 "+ str() + " 字。")