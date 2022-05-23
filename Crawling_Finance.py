import requests
import os
import time
from selenium import webdriver
from bs4 import BeautifulSoup as bf

class Crawling_Finance():
    def __init__(self):
        self.GetHtml_NaverFinance()

    def GetHtml_NaverFinance(self):
        self.req = requests.get('https://finance.naver.com/sise/')
        self.html = self.req.text
        self.soup = bf(self.html, 'html.parser')

    # 네이버 인기 종목 주식 정보 ~10위
    # return [{종목 : 시세}, 상승or하락]
    def Crawling_PopularStocks(self):
        stockName_soup = self.soup.select('.lst_pop > li > a')  #.클래스 이름
        stockValue_soup = self.soup.select('.lst_pop > li > span')
        stockUpDown_soup = self.soup.select('.lst_pop > li > em > span')

        liStockInfo_Naver = []
        for i in range (len(stockName_soup)) :
            dicNameValue_Stock = {}
            dicNameValue_Stock[stockName_soup[i].text] = (stockValue_soup[i].text)
            liStockInfo = []
            liStockInfo.append(dicNameValue_Stock)
            liStockInfo.append(stockUpDown_soup[i].text)
            liStockInfo_Naver.append(liStockInfo)

        return liStockInfo_Naver

    # 코스피 정보
    # return [코스피지수, 변화율(숫자), 변화율(%)]
    def Crawling_Kospi(self):
        strKOSPI = self.soup.find(id = 'KOSPI_now').string
        strKOSPI_Change_Percent = self.soup.find(id = 'KOSPI_change').contents[2]
        strKOSPI_Change = strKOSPI_Change_Percent.split()[0]
        strKOSPI_Percent = strKOSPI_Change_Percent.split()[1]
        liKospi = [strKOSPI, strKOSPI_Change, strKOSPI_Percent]
        return liKospi
        #print(strKOSPI)
        #print(strKOSPI_Change)

    # 코스닥 정보
    # return [코스닥지수, 변화율(숫자), 변화율(%)]
    def Crawling_Kosdaq(self):
        strKOSDAQ = self.soup.find(id = 'KOSDAQ_now').string
        strKOSDAQ_Change_Percent = self.soup.find(id = 'KOSDAQ_change').contents[2]
        strKOSDAQ_Change = strKOSDAQ_Change_Percent.split()[0]
        strKOSDAQ_Percent = strKOSDAQ_Change_Percent.split()[1]
        liKosdaq = [strKOSDAQ, strKOSDAQ_Change, strKOSDAQ_Percent]
        return liKosdaq
        #print(strKOSDAQ)
        #print(strKOSDAQ_Change)

    # 종목 검색
    # return df(pandas)
    def Search_StockandCrawling(self, strStockName):
        # Selenium Option 설정
        Selenium_Option = webdriver.ChromeOptions()
        Selenium_Option.add_argument('headless')    # 창 안뜨게 함.
        Selenium_Option.add_argument('window-size=1920x1080')   # 창 크기 조절
        Selenium_Option.add_argument('disable-gpu')

        # Chromedriver 가져오기.
        self.strStockName = strStockName
        strChromedriverName = "chromedriver.exe"
        strPath = os.getcwd()
        driver = webdriver.Chrome(strPath + "//" + strChromedriverName)
        driver.implicitly_wait(1)

        # 실행
        driver.get('https://finance.naver.com/sise/')
        driver.implicitly_wait(1)
        Search_Input = driver.find_element_by_class_name("snb_search_text")
        Search_Input.send_keys(self.strStockName)   # 종목 적음.
        Search_Input.submit()                       # 검색 클릭.
        driver.implicitly_wait(1)

        # thead Parsing
        table = driver.find_element_by_class_name("tbl_search")
        thead = table.find_element_by_tag_name("thead")
        il_thead_th = thead.find_elements_by_tag_name("th")

        # tbody Parsing
        tbody = table.find_element_by_tag_name("tbody")
        li_tbody_tr = tbody.find_elements_by_tag_name("tr")
        li_tbody_td = []
        for i in range(len(li_tbody_tr)):
            tbody_tr = li_tbody_tr[i]
            li_tbody_td.append(tbody_tr.find_elements_by_tag_name("td"))
        # li_tbody_td = [[0],[1],[2]...]
        
        # list 안의 데이터 .text 읽어와서 pandas 를 통해
        # dataframe 만들기.



