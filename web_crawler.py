"""Module to crawl websites"""

from __future__ import annotations

import os
import time
import traceback
from collections import deque

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

from configs import Configs
from utils import Utils
from html_parser import HtmlParser


class WebCrawler:
    """WebCrawler Module"""

    def __init__(self):
        self.queue = deque()
        self.visited = set()
        self.parser = HtmlParser()
        self.utils = Utils()


    def dump_data(self):
        pass


    def load_data(self):
        pass


    def crawl_website(self):
        """Crawls entire website one url at a time and saves
        theit content in doc files in DATA_DIR.
        """
        self.queue.append(Configs.PAGE_URL)
        while len(self.queue):
            web_url = self.queue.popleft()

            if web_url in self.visited:
                continue

            page_source, links = self.crawl_url(web_url)
            result = self.parser.parse_webpage_basic(page_source)
            if result:
                self.utils.write_docs(result, web_url)
            self.visited.add(web_url)
            for link in links:
                if link not in self.visited:
                    self.queue.append(link)

            # print(result)
            break

        return None


    def crawl_url(self, url):
        """_summary_

        Args:
            url (str): the url that needs to be crawled

        Returns:
            webElements or None: page source of url
        """
        page_source, links = None, []
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            wait = WebDriverWait(driver, Configs.MAX_WAITING_TIME)
            wait.until(EC.visibility_of_all_elements_located((By.ID, Configs.PAGE_COMMON_ID)))
            time.sleep(5)

            page_source = driver.page_source
            links = [self.utils.preprocess_web_url(anchor.get_attribute('href')) for anchor in driver.find_elements(by=By.TAG_NAME, value="a") if anchor.get_attribute('href') is not None]
        except Exception as ex:
            print(traceback.print_exc())
            return page_source, links
        finally:
            driver.close()

        return page_source, links
    

if __name__ == '__main__':
    crawler = WebCrawler()
    crawler.crawl_website()
