from attr import asdict
import requests
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bf

class Crawling_News():
    def Search_NaverNews(self, strKeyWard, strPeriod):
        self.strKeyWard = strKeyWard
        self.strPeriod = strPeriod

        # Selenium Option 설정
        Selenium_Option = webdriver.ChromeOptions()
        Selenium_Option.add_argument('headless')    # 창 안뜨게 함.
        Selenium_Option.add_argument('window-size=1920x1080')   # 창 크기 조절
        Selenium_Option.add_argument('disable-gpu')

        # Chromedriver 가져오기.
        strChromedriverName = "chromedriver.exe"
        strPath = os.getcwd()
        driver = webdriver.Chrome(strPath + "\\" + strChromedriverName)
        driver.implicitly_wait(3)

        # Chrome Driver 실행
        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + strKeyWard + "&start=" + "1"
        driver.get(url)
        driver.implicitly_wait(3)

        # 검색 옵션 클릭.
        Search_Input = driver.find_element_by_class_name("option_filter")
        time.sleep(1)
        Search_Input.click()
        driver.implicitly_wait(3)
        
        # 뉴스 적용 기간 설정
        strPeriod_Setting = ""
        if (self.strPeriod == 'day'):
            strPeriod_Setting = "1일"
        elif (self.strPeriod == 'week'):
            strPeriod_Setting = "1주"
        elif (self.strPeriod == 'month'):
            strPeriod_Setting = "1개월"
        else:
            strPeriod_Setting = "1년"

        btnPeriod = driver.find_element_by_link_text(strPeriod_Setting)
        btnPeriod.click()
        driver.implicitly_wait(3)

        # 네이버 뉴스 기사 Search
        btnNaverNews = driver.find_elements_by_link_text("네이버뉴스")
        for NaverNews in btnNaverNews:
            NaverNews.click()
            strNewTab = driver.window_handles[-1]
            driver.switch_to.window(strNewTab)
            a = 1





        
