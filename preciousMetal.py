import scrapy
from scrapy.crawler import CrawlerProcess
from random import randrange
import logging
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which
import time

from scrapy import Selector


class preciousMetalSpiderSelenium(scrapy.Spider):
    name = 'preciousMetal'

    start_urls= ["https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table"]

    metal = " platinum "

    fileName = metal + '_Data.csv'

    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': fileName,
        'CONCURRENT_REQUESTS': '1',
        # 'FEED_EXPORT_ENCODING': 'utf-8'
    }

    def parse(self, response):
        chromeOptions = Options()
        #chromeOptions.add_argument("--headless")
        chrome_path = which("chromedriver")
        driver = webdriver.Chrome(executable_path=chrome_path, options=chromeOptions)
        driver.set_window_size(1920, 1080)
        driver.get("https://www.lbma.org.uk/prices-and-data/precious-metal-prices#/table")
        time.sleep(5)

        metal = ' Platinum '

        select = driver.find_element_by_xpath("(//span[@class='caret']/*[name()='svg'])[1]").click()
        time.sleep(5)
        metalSelect= driver.find_element_by_xpath("(//ul[@class='dropdown-menu']/li/a[text()='"+metal+"'])[1]").click()

        time.sleep(3)

        self.html = driver.page_source
        response = Selector(text=self.html)

        select2 = driver.find_element_by_xpath("(//span[@class='caret']/*[name()='svg'])[2]").click()
        time.sleep(3)
        self.html = driver.page_source
        response = Selector(text=self.html)
        years = response.xpath("(//ul[@class='dropdown-menu']/li/a/text())").getall()
        select2 = driver.find_element_by_xpath("(//span[@class='caret']/*[name()='svg'])[2]").click()

        print("years data extracted...")
        print(years)
        time.sleep(3)

        for year in years:
            yearNew = year.strip();
            yearNew = int(yearNew)

            if yearNew >= 2010 and yearNew <= 2011:
                select2 = driver.find_element_by_xpath("(//span[@class='caret']/*[name()='svg'])[2]").click()
                print("Drop menu clicked ...")
                print("year selected..." + year)
                time.sleep(3)
                yearSelect = driver.find_element_by_xpath("(//ul[@class='dropdown-menu']/li/a[text()='" + year + "'])[1]").click()
                time.sleep(3)

                self.html = driver.page_source
                response = Selector(text=self.html)

                rows = response.xpath("//tbody/tr")

                for row in rows:
                    date = response.xpath(".//td[@class='-index0']/text()").get()
                    usdAm = response.xpath(".//td[@class='-index1']/text()").get()
                    usdPm = response.xpath(".//td[@class='-index2']/text()").get()
                    gbpAm = response.xpath(".//td[@class='-index3']/text()").get()
                    gbpPm = response.xpath(".//td[@class='-index4']/text()").get()
                    eurAm = response.xpath(".//td[@class='-index5']/text()").get()
                    eurPm = response.xpath(".//td[@class='-index6']/text()").get()

                    yield {
                        'Date': date,
                        'USD AM': usdAm,
                        'USD PM': usdPm,
                        'GBP AM': gbpAm,
                        'GBP PM': gbpPm,
                        'EUR AM': eurAm,
                        'EUR PM': eurPm,
                    }

process = CrawlerProcess()
process.crawl(preciousMetalSpiderSelenium)
process.start()