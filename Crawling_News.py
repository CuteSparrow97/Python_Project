from attr import asdict
import requests
import os
import time
import pandas as pd
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bf

class Crawling_News():
    def Search_NaverNews(self, strKeyWard, strPeriod, nPage):
        self.strKeyWard = strKeyWard
        self.strPeriod = strPeriod
        self.nPage = nPage

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
        
        # 네이버 뉴스 URL Parsing
        Pages_URL = []
        naver_urls=[]
        for i in range(self.nPage):
            # 네이버 기사가 있는 css selector 모아오기
            News = driver.find_elements(By.CSS_SELECTOR,'a.info')
            # 위에서 생성한 css selector list 하나씩 클릭하여 본문 url 얻기
            for NewsURL in News:
                NewsURL.click()
                # 현재 탭에 접근
                driver.switch_to.window(driver.window_handles[1])
                time.sleep(3) #대기시간 변경 가능
                # 네이버 뉴스만 가져오기
                url = driver.current_url
                print(url)
                if "news.naver.com" in url:
                    naver_urls.append(url)
                else:
                    pass
                # 현재 탭 닫기
                driver.close()
                # 다시 처음 탭으로 돌아가기
                driver.switch_to.window(driver.window_handles[0])

            # 페이지 없을 경우 대비
            try:
                btnPage = driver.find_element_by_link_text(str(i + 2))
                btnPage.click()
            except Exception as error:
                print('Page 문제 발생(원하는 Page를 찾을 수 없음)', error)
                continue

        # ConnectionError방지
        headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }
        titles = []
        contents = []
        # 네이버 뉴스 기사 Search
        # libtnNaverNews = driver.find_elements_by_link_text("네이버뉴스")
        for url in naver_urls:
            # NaverNews.click()
            # strNewTab = driver.window_handles[-1]
            # driver.switch_to.window(strNewTab)

            # Request를 사용하여 해당 url을 사용 친화적으로 만든다.
            req = requests.get(url, headers=headers)

            # requests_text 함수를 이용하여 현재 url 정보를 html로 받음
            html = bf(req.text, "html.parser")

            # 뉴스 제목 가져오기
            title = html.select("div#ct > div.media_end_head.go_trans > div.media_end_head_title > h2")
            # list 합치기.
            title = ''.join(str(title))
            # html 태그 제거
            pattern1 = '<[^>]*>'
            title = re.sub(pattern=pattern1, repl='', string = title)
            titles.append(title)

            # 뉴스 본문
            content = html.select("div#dic_area")
            # 리스트 합치기
            content = ''.join(str(content))
            # html 태그제거 및 텍스트 다듬기
            content = re.sub(pattern=pattern1, repl='', string=content)
            pattern2 = """[\n\n\n\n\n// flash 오류를 우회하기 위한 함수 추가\nfunction _flash_removeCallback() {}"""
            content = content.replace(pattern2,'')
            contents.append(content)

            # driver.close()
            # strNewTab = driver.window_handles[0]
            # driver.switch_to.window(strNewTab)

        print(titles)
        print(contents)

        news_df = pd.DataFrame({'title':titles,'link':naver_urls,'content':contents})
        news_df.to_csv("C:\\Users\\LCH\Desktop\\test_News.csv",",","NaN", index=False, encoding='utf-8-sig')
        #news_df.to_csv("C:\\Users\\dlckd\Desktop\\test1.csv",",","NaN", index=False, encoding='utf-8-sig')


        
