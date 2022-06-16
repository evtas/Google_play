from concurrent.futures import thread
from telnetlib import EC
from selenium import webdriver
import psycopg2
import time
import queue    
from threading import Thread, Semaphore
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

BASE_URL = "https://apkcombo.com/zh/"

class ApksCrawler(object):
    def __init__(self):
        self.sem = Semaphore(16)

    def get_urls(self):
        conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
        cur = conn.cursor()

        sql = "select url from google_play_games"
        cur.execute(sql)
        urls = cur.fetchall() 
        conn.close()
        
        return urls
    
    def crawl(self, origin_url):
        web_driver = webdriver.Chrome(executable_path='/Users/Ben/chromedriver')
        # web_driver.maximize_window()

        url = BASE_URL + origin_url[0][46:]
        print(url)

        web_driver.get(url)
        WebDriverWait(web_driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='qc-cmp2-ui']/div[2]/div/button[1]")))

        download_link = ""
        # apk_crawl_2
        try:
            # 弹窗
            web_driver.find_element_by_xpath("//*[@id='qc-cmp2-ui']/div[2]/div/button[1]").click()
            WebDriverWait(web_driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='main']/div[1]/div/div[1]/div[2]/div[2]/div/a")))

            link = web_driver.find_element(by=By.XPATH, value="//*[@id='main']/div[1]/div/div[1]/div[2]/div[2]/div/a")

            print(link)

            if not link.get_attribute('innerText') == 'Play Store':
                link.click()

            WebDriverWait(web_driver, 10, 0.5).until(EC.presence_of_element_located((By.XPATH, "//*[@id='best-variant-tab']/div[1]/ul/li/ul/li/a")))
            download_link = web_driver.find_element_by_xpath("//*[@id='best-variant-tab']/div[1]/ul/li/ul/li/a").get_attribute('href')
        except:
            print('dont have this apk')
        finally:
            web_driver.quit()

        print("download_link: ", download_link)
        if download_link:
            try:
                # 更新apk信息    
                conn = psycopg2.connect(database="google_play", user="postgres", password="binshao123", host="127.0.0.1", port="5432")
                cur = conn.cursor()
                cur.execute('update google_play_games set apk = %s where url = %s', (download_link, origin_url))
                conn.commit()
                print('update_success')
            except:
                print('update_failer')

        self.sem.release()

    def start(self):
        urls = self.get_urls()
        count = 0
        for origin_url in urls:
            print(count)
            count+=1
            if count <= 12485:
                continue
            
            self.sem.acquire()
            t = Thread(target=self.crawl, args=(origin_url,))
            t.start()
            

if __name__ == '__main__':
    sem = Semaphore()
    ac = ApksCrawler()
    ac.start()



