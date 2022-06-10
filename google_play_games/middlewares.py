# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from google_play_games import settings
import random
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains

import time
from scrapy.http import HtmlResponse




class GooglePlayGamesSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class GooglePlayGamesDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class selMiddleware(object):
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path='/Users/Ben/chromedriver')
        self.driver.maximize_window()


    def process_request(self, request, spider):
        if not "id=" in request.url:
            self.driver.get(request.url)
            time.sleep(1)

            # 免费，获利最高，热门付费
            # 第一个操作是这个，如果第一个操作先下滑，这个操作会有bug
            try:    
                button_2 = self.driver.find_elements_by_xpath("//div[@class='b6SkTb']/div/div[2]/span[2]")
                for b in button_2:
                    b.click()
                    time.sleep(1)
            except:
                pass

            # 下滑
            js = "document.documentElement.scrollTop=20000"
            for i in range(7):
                self.driver.execute_script(js)
                time.sleep(1)
            
            # 显示更多内容
            try:
                button_1 = self.driver.find_element_by_xpath("//*[contains(text(), '显示更多内容')]")
                button_1.click()
                
                js = "document.documentElement.scrollTop=20000"
                for i in range(3):
                    self.driver.execute_script(js)
                    time.sleep(1)
            except:
                pass

            # 往右滑
            scroll_right_items = self.driver.find_elements_by_xpath("//div[@class='bewvKb']")
            print(len(scroll_right_items))

            for i in range(len(scroll_right_items)):
                print(i)
                try:
                    ActionChains(self.driver).move_to_element(scroll_right_items[i]).perform()
                    time.sleep(0.2)

                    while scroll_right_items[i].find_element_by_xpath("//*[contains(text(), 'chevron_right')]"):
                        button = scroll_right_items[i].find_element_by_xpath("//*[contains(text(), 'chevron_right')]")
                        # print(button)
                        if button.is_displayed():
                            button.click()
                        else:
                            break
                        time.sleep(0.2)
                except:
                    pass
            

            body = self.driver.page_source

            print("访问" + request.url)

            return HtmlResponse(self.driver.current_url, body=body, encoding='utf-8', request=request)