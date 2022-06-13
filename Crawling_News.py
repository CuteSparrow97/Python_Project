import requests
import os
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bf

class Crawling_News():
    def Search_NaverNews(self, strKeyWard):
        # Selenium Option 설정
        #Selenium_Option = webdriver.ChromeOptions()
        #Selenium_Option.add_argument('headless')    # 창 안뜨게 함.
        #Selenium_Option.add_argument('window-size=1920x1080')   # 창 크기 조절
        #Selenium_Option.add_argument('disable-gpu')
        #
        ## Chromedriver 가져오기.
        #self.strKeyWard = strKeyWard
        #strChromedriverName = "chromedriver.exe"
        #strPath = os.getcwd()
        #driver = webdriver.Chrome(strPath + "//" + strChromedriverName)
        #driver.implicitly_wait(1)
#
        ## Chrome Driver 실행
        #driver.get('https://news.naver.com/')
        #driver.implicitly_wait(1)
        #Search_Icon = driver.find_element_by_xpath("/html/body/section/header/div[1]/div/div/div[2]/div[3]/a")
        #Search_Icon.click();
        #driver.implicitly_wait(1)
        #Search_Input = driver.find_element_by_xpath('//*[@id="u_hs"]/div/div/input')
        #Search_Input.send_keys(self.strKeyWard)
        #Search_Input.submit()                     
        #driver.implicitly_wait(1)
#
        #articles = driver.find_elements_by_class_name("news_area")
        #a = 1;

        url = "https://search.naver.com/search.naver?where=news&sm=tab_pge&query=" + strKeyWard + "&start=" + "1"
        print("생성url: ",url)

        # ConnectionError방지
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/100.0.48496.75" }

        #html불러오기
        original_html = requests.get(url, headers=headers)
        html = bf(original_html.text, "html.parser")

        # 검색결과
        articles = html.select("div.group_news > ul.list_news > li div.news_area > a")
        print(articles)
        # 검색된 기사의 갯수
        print(len(articles),"개의 기사가 검색됌.")

        #뉴스기사 제목 가져오기
        news_title = []
        for i in articles:
            news_title.append(i.attrs['title'])
        news_title

        #뉴스기사 URL 가져오기
        news_url = []
        for i in articles:
            news_url.append(i.attrs['href'])
        news_url

        #뉴스기사 내용 크롤링하기
        contents = []
        for i in news_url:
            #각 기사 html get하기
            news = requests.get(i,headers=headers)
            news_html = bf(news.text,"html.parser")
            #기사 내용 가져오기 (p태그의 내용 모두 가져오기) 
            contents.append(news_html.find_all('p'))
        contents
        
