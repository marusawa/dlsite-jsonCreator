import requests
from bs4 import BeautifulSoup
import json

def get_dlsite_pinfo(productID):

    ##########################################################
    urlMain = "https://www.dlsite.com/maniax/work/=/product_id/"
    urlExt = ".html"
    urlName = urlMain + productID + urlExt
    url = requests.get(urlName)
    soup = BeautifulSoup(url.content,"html.parser")
    ##########################################################

    #取得しない作品情報
    noGetList = ["最終更新日","ファイル容量", "ファイル形式"]

    #タイトルとサークル名取得
    title = soup.find_all("h1",{"id":"work_name"})[0].get_text()
    circle = soup.find_all("span",{"class":"maker_name"})[0].get_text()
    #タイトルとサークル名出力
    title = title.replace('\n','')
    circle = circle.replace('\n','')

    #作品情報取得
    workTable = soup.find_all("table",{"id":"work_outline"})[0]
    rows = workTable.findAll("tr")
    for row in rows:
        try:
            heads = row.findAll("th")
            docs = row.findAll("td")
            for head in heads:
                hStr = head.get_text().replace('\n','')
                mHStr = " "
            if hStr not in noGetList:
                for doc in docs:
                    elems = doc.findAll("a")
                    dList = ""
                    for elem in elems:
                        if hStr != mHStr:
                            mHStr = hStr
                            dList = elem.get_text().replace('\n','')
                        else:
                            dList = dList + "," + elem.get_text().replace('\n','')
                    #作品情報出力
                    #print(hStr + ":" + dList)
                    if   hStr == "販売日" :
                        lstRelaseDate = dList.split(',')
                    elif hStr == "シナリオ" :
                        lstScenarioWriter = dList.split(',')
                    elif hStr == "イラスト" :
                        lstIllustrator = dList.split(',')
                    elif hStr == "声優" :
                        lstActor = dList.split(',')
                    elif hStr == "作品形式" :
                        lstProductType = dList.split(',')
                    elif hStr == "ジャンル" :
                        lstGenre = dList.split(',')
        except:
            pass

    dic = {
        "rjNumber"     : productID,
        "title"        : title,
        "circle"       : circle,
        "releaseDate"  : lstRelaseDate,
        "scenario"     : lstScenarioWriter,
        "illust"       : lstIllustrator,
        "voiceActor"   : lstActor,
        "productType"  : lstProductType,
        "genre"        : lstGenre
    }

    jsonString = json.dumps(dic, ensure_ascii=False, indent=2)
    return jsonString

#情報を取得する作品ID
# For example:
# productID = 'RJ310349'
# createdJson = get_dlsite_pinfo(productID)
# print(createdJson)
