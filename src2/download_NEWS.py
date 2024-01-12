from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import os
from bs4 import BeautifulSoup

def make_html_file(filelocation, title, content):
    title_soup = BeautifulSoup(str(title), 'html.parser')
    content_soup = BeautifulSoup(str(content), 'html.parser')

    # Extract the HTML content from the title and content divs
    title_html = title_soup.prettify()
    content_html = content_soup.prettify()

    # Combine title and content
    text = title_html + content_html
    # text = title + content
    script_dir = os.path.dirname(__file__)
    rel_path = "../download/NEWS/" + filelocation + ".html"
    abs_file_path = os.path.join(script_dir, rel_path)
    with open(abs_file_path, "w", encoding='utf-8') as f:
        f.write(text)

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

def handle_news_list_file(dirname):
    if not os.path.isdir("../download/NEWS/" + dirname):
        os.mkdir(os.path.dirname(__file__) + "/../download/NEWS/" + dirname)
        
    driver.get("https://finance.eastmoney.com/a/" + dirname + ".html")
    wait = WebDriverWait(driver, 10)
    news_list_content = wait.until(EC.presence_of_element_located((By.ID, 'newsListContent')))
    wait.until(EC.presence_of_all_elements_located((By.XPATH, './/li',)), "Sub-elements not loaded")

    content_body = driver.find_element(By.ID, 'newsListContent')
    li_elements = content_body.find_elements(By.TAG_NAME, 'li')
    for li_element in li_elements:
        anchor_tag = li_element.find_element(By.TAG_NAME, 'a')
        anchor_link = anchor_tag.get_attribute('href')
        url_parts = anchor_link.split('/')

        driver.get(anchor_link)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, 'topbox')))
        filelocation = dirname + '/' + url_parts[-1].split('.')[0]
        title = driver.find_element(By.ID, 'topbox')
        content = driver.find_element(By.ID, 'ContentBody')
        make_html_file(filelocation, title, content)

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
