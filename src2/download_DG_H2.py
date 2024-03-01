import os, json, requests, math, tqdm, multiprocessing
import sys, time
from os.path import exists
from datetime import datetime, timedelta, date

def dl_PDF(jsItem, url_fc='', path='', filename=''):
    os.makedirs(path, exist_ok = True)
    # print("downloading " + filename + "...")
    try:
        r = requests.get(url_fc,
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                                'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
            },
            timeout=10
        )
        fname = os.path.join(path + "/",filename)
        with open(fname, 'wb') as fd:
            fd.write(r.content)
        return True
    except:
        return False

def get_url_for_report_dg(pn=1):
    siteURL = 'https://np-anotice-stock.eastmoney.com/api/security/ann'
    para = {
        'sr': -1,
        'page_size': 50,
        'page_index': pn,
        'ann_type': 'A',
        'f_node': 1,
        's_node': 1
    }
    return requests.Request('GET', url=siteURL, params=para).prepare().url

def get_json_array(pn=1):
    r = requests.get(get_url_for_report_dg(pn=pn),
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                            'like Gecko) Chrome/81.0.4044.138 Safari/537.36 Edg/81.0.416.77'
        },
        timeout=10000
    ).json()
    return r['data']['list']

def core_DG(item):
    path = "../download/DG_H2/report"
    if item['columns'][0]['column_code'] in ['001001001001001', '001001001002001', '001001001003001', '001001001004001']:
        dl_PDF(
            item,
            url_fc= 'http://pdf.dfcfw.com/pdf/H2_'+item['art_code']+'_1.pdf',
            path = path,
            filename = item['art_code']+'.pdf'
        )

def main_DG():
    print("Starting DG_H2 report download...")
    # checking if download folder exists or not.
    if not os.path.isdir("../download"):
        os.mkdir(os.path.dirname(__file__) + "/../download")
    if not os.path.isdir("../download/DG_H2"):
        os.mkdir(os.path.dirname(__file__) + "/../download/DG_H2")

    # make hyyb record list file
    print("Starting record json_array download...")
    print("Writing record.txt file...")

    total_pages = 100
    
    with open("../download/DG_H2/record.txt", "w") as f:
        f.write('[')
        for i in tqdm.tqdm(range(total_pages)):
            page_number = i + 1
            # print("writing page" + str(page_number) + "...")
            list_response = get_json_array(pn=page_number)
            count = 1
            list_length = len(list_response)
            for item in list_response:
                f.write(json.dumps(item))
                if (page_number != total_pages):
                    f.write(',')
                else:
                    if (count != list_length):
                        f.write(',')
                count += 1

        f.write(']')
    
    print('Finished record list download successfully!')

    # download record pdf files
    print("Starting report files download...")
    with open("../download/DG_H2/record.txt", "r") as f:
        all_list = f.read()

    list = json.loads(all_list)
    path = "../download/DG_H2/report"
    os.makedirs(path, exist_ok = True)
    multiprocessing.freeze_support()
    pool = multiprocessing.Pool(processes=10)
    for _ in tqdm.tqdm(pool.imap_unordered(core_DG, list), total=len(list)): pass
    
    print("Finished report file download successfully!")
    print("----------------------------------------------")

if __name__ == "__main__":
    main_DG()