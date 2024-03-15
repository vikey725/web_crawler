"""Module to crawl websites"""

from __future__ import annotations

import os
import time
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


    def dump_data(self):
        pass


    def load_data(self):
        pass


    def crawl_website(self):
        """Crawls entire website one url at a time and saves
        theit content in doc files in DATA_DIR.
        """
        self.queue.append(Configs.BASE_URL)
        while len(self.queue):
            web_url = self.queue.popleft()

            if web_url in self.visited:
                continue

            page_source = self.crawl_url(web_url)

        return None


    def crawl_url(self, url):
        """_summary_

        Args:
            url (str): the url that needs to be crawled

        Returns:
            webElements or None: page source of url
        """
        page_source = None
        try:
            driver = webdriver.Chrome()
            driver.get(url)
            wait = WebDriverWait(driver, Configs.MAX_WAITING_TIME)
            wait.until(EC.visibility_of_all_elements_located((By.ID, Configs.PAGE_COMMON_ID)))
            driver.implicitly_wait(10)

            page_source = driver.page_source
        except Exception as ex:
            print(ex)
            return page_source
        finally:
            driver.close()

        return page_source
