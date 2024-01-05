from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import requests
import os
import json
import tqdm, multiprocessing
from bs4 import BeautifulSoup
from datetime import datetime, timedelta, date
import EM_TOOL

# def url(ide='0000012'):
#     # siteURL = 'http://f10.eastmoney.com/NewsBulletin/NewsBulletinAjax'
#     siteURL = 'http://emweb.eastmoney.com/PC_HSF10/NewsBulletin/PageAjax'
#     para = {
#         'code': EM_TOOL.IDE2SID(ide)
#     }
#     return requests.Request('GET', url=siteURL, params=para).prepare().url

# def parser(content,ide):
#     js = json.loads(content)
#     xx = js['gszx']['data']['items']
#     request = []
#     for record in xx:
#         # del record['url'], record['code'], record['recordId'], record['source'], record['updateTime']
#         # del record['publishDate'], record['sRatingName']
#         request.append(pymongo.UpdateOne(
#             {"IDE":ide,"infoCode":record['infoCode']},
#             {"$set":record},
#             upsert=True 
#         ))
#     if request: MDB.col_NOTICE_ZIXUN.bulk_write(request)


#     # gg = js['gsgg']['data']['items']
#     gg = js['gsgg']
#     request = []
#     for record in gg:
#         # del record['uniqueUrl'],record['url'], record['code'], record['recordId'], record['source']
#         # del record['updateTime'],record['showDateTime'], record['sRatingName'], record['summary']
#         request.append(pymongo.UpdateOne(
#             {"IDE":ide,"infoCode":record['art_code']},
#             {"$set":record},
#             upsert=True 
#         ))
#     if request: MDB.col_NOTICE_GONGGAO.bulk_write(request)
#     return True

# def down_ZIXUN(item):
#     from bs4 import BeautifulSoup
#     try:
#         try:
#             r = requests.get(
#                 item['uniqueUrl'], 
#                 headers ={
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
#                                 'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
#                 },
#                 allow_redirects=False
#             )
#         except:
#             r = requests.get(
#                 item['url'], 
#                 headers ={
#                     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
#                                 'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
#                 },
#                 allow_redirects=True,
#                 timeout=1
#             )            
#         if (r.status_code == 200):
#             ContentBody = BeautifulSoup(r.content, 'html.parser').find(id='ContentBody')   
#             ps = []
#             for p in ContentBody.find_all('p'): 
#                 ps.append(p.text)
#             ps = '\n'.join(ps)
#             # print(ps)
#             MDB.col_NOTICE_ZIXUN.update_one({"IDE":item['IDE'],"infoCode":item['infoCode']},{"$set":{"content":ps}},)
#     except:
#         pass





# def fetch_push(ide): 
#     r = requests.get(url(ide=ide), 
#         headers = {
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML  '
#                             'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
#         }, 
#         timeout=10
#     )
#     return parser(r.content,ide)
# # print(fetch_push("0000012"))

# def make_news_text_file(filename, data):
#     # print("make text file for QUATE_" + filename + "...")
#     text = json.dumps(data)
#     script_dir = os.path.dirname(__file__)
#     rel_path = "../download/QUATE/QUATE_" + filename + ".txt"
#     abs_file_path = os.path.join(script_dir, rel_path)
#     with open(abs_file_path, "w") as f:
#         f.write(text)
#     # print("QUATE_" + filename + " file was made successfully!")

# def download_news_data(stock):
#     parser = configparser.ConfigParser()
#     parser.read('config.ini')
#     response = fetch_dk_push(stock["IDE"])
#     make_news_text_file(stock["IDE"], response)

# options = webdriver.ChromeOptions()
# options.add_argument('--headless')
# driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)

def handle_news_list_file(dirname):
    if not os.path.isdir("../download/NEWS/" + dirname):
        os.mkdir(os.path.dirname(__file__) + "/../download/NEWS/" + dirname)
        
    # driver.get("https://finance.eastmoney.com/a/" + dirname + ".html")
    # driver.implicitly_wait(5)
    # html_content = driver.page_source
    r = requests.get(
        "https://finance.eastmoney.com/a/" + dirname + ".html", 
        headers ={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                        'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
        },
    )
    if (r.status_code == 200):
        # soup = BeautifulSoup(html_content, 'html.parser')
        soup = BeautifulSoup(r.content, 'html.parser')
        ContentBody = soup.find(id='newsListContent')
        if ContentBody:
            # Find all <li> elements within each <ul> element
            li_elements = ContentBody.find_all('li')
            # Extract and print anchor links within each <li> element
            for li_element in li_elements:
                anchor_tag = li_element.find('a')
                if anchor_tag:
                    anchor_link = anchor_tag.get('href')
                    print(anchor_link)
        
    # list = []
    # multiprocessing.freeze_support()
    # pool = multiprocessing.Pool(processes=10)
    # for _ in tqdm.tqdm(pool.imap_unordered(download_news_data, list), total=len(list)): pass

def main_NEWS():
    print("Starting NEWS download...")
    # checking if download folder exists or not.
    if not os.path.isdir("../download"):
        os.mkdir(os.path.dirname(__file__) + "/../download")
    if not os.path.isdir("../download/NEWS"):
        os.mkdir(os.path.dirname(__file__) + "/../download/NEWS")

    print("Starting cgjjj download...")
    handle_news_list_file("cgjjj")
    print("Finished cgjjj download successfully!")
    
    print("Starting cgnjj download...")
    handle_news_list_file("cgnjj")
    print("Finished cgnjj download successfully!")
    
    print("Starting ccjxw download...")
    handle_news_list_file("ccjxw")
    print("Finished ccjxw download successfully!")
    
    print("Starting czsdc download...")
    handle_news_list_file("czsdc")
    print("Finished czsdc download successfully!")
    
    print("Starting ccjdd download...")
    handle_news_list_file("ccjdd")
    print("Finished ccjdd download successfully!")
    
    print("Starting crdsm download...")
    handle_news_list_file("crdsm")
    print("Finished crdsm download successfully!")
    
    print("Starting chgyj download...")
    handle_news_list_file("chgyj")
    print("Finished chgyj download successfully!")
    
    print("Starting pinglun download...")
    handle_news_list_file("pinglun")
    print("Finished pinglun download successfully!")
    
    print("Finished NEWS download successfully!")
    print("-------------------------------------------------")

if __name__ == "__main__":
    main_NEWS()
