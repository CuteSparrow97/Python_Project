from asyncio.windows_events import NULL
import requests
import os
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
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
    def Search_NaverStock(self, strStockName):
        # Selenium Option 설정
        Selenium_Option = webdriver.ChromeOptions()
        Selenium_Option.add_argument('headless')    # 창 안뜨게 함.
        Selenium_Option.add_argument('window-size=1920x1080')   # 창 크기 조절
        Selenium_Option.add_argument('disable-gpu')

        # Chromedriver 가져오기.
        self.strStockName = strStockName
        strChromedriverName = "chromedriver.exe"
        strPath = os.getcwd()
        driver = webdriver.Chrome(strPath + "\\" + strChromedriverName)
        driver.implicitly_wait(1)

        # Chrome Driver 실행
        driver.get('https://finance.naver.com/sise/')
        driver.implicitly_wait(1)
        Search_Input = driver.find_element_by_class_name("snb_search_text")
        Search_Input.send_keys(self.strStockName)   # 종목 적음.
        Search_Input.submit()                       # 검색 클릭.
        driver.implicitly_wait(1)

        # thead Parsing
        table = driver.find_element_by_class_name("tbl_search")
        thead = table.find_element_by_tag_name("thead")
        li_thead_th = thead.find_elements_by_tag_name("th")

        # tbody Parsing
        tbody = table.find_element_by_tag_name("tbody")
        li_tbody_tr = tbody.find_elements_by_tag_name("tr")
        li_tbody_td = []
        for i in range(len(li_tbody_tr)):
            tbody_tr = li_tbody_tr[i]
            tbody_td = tbody_tr.find_elements_by_tag_name("td")
            li_tbody_td.append(tbody_td)
            # li_tbody_td = [Row1[title, price..],Row2[title, price],...]
        
        # Create DataFrame(table)
        df = pd.DataFrame()
        li_data = []
        for i in range(len(li_thead_th)):
            for j in range(len(li_tbody_td)):
                li_data.append(li_tbody_td[j][i].text)

            a = 1
            df[li_thead_th[i].text] = li_data
            li_data.clear()
            
        # csv output
        df.to_csv("C:\\Users\\LCH\Desktop\\test1.csv",",","NaN",encoding="utf-8-sig")
        # df.to_csv("C:\\Users\\dlckd\Desktop\\test1.csv",",","NaN",encoding="utf-8-sig")
        
        # list 안의 데이터 .text 읽어와서 pandas 를 통해
        # dataframe 만들기.
    
    def Search_hankyung(self, strStockName):
         # Selenium Option 설정
        Selenium_Option = webdriver.ChromeOptions()
        Selenium_Option.add_argument('headless')    # 창 안뜨게 함.
        Selenium_Option.add_argument('window-size=1920x1080')   # 창 크기 조절
        Selenium_Option.add_argument('disable-gpu')

         # Chromedriver 가져오기.
        self.strStockName = strStockName
        strChromedriverName = "chromedriver.exe"
        strPath = os.getcwd()
        driver = webdriver.Chrome(strPath + "\\" + strChromedriverName)
        driver.implicitly_wait(1)

        # Chrome Driver 실행
        driver.get('http://hkconsensus.hankyung.com/apps.analysis/analysis.list?skinType=business')
        driver.implicitly_wait(1)
        Search_Input = driver.find_element_by_id("search_text")
        Search_Input.send_keys(self.strStockName)   # 종목 적음.
        
        # 날짜 변경
        StartDateText = driver.find_element_by_id("sdate")
        StartDateText.click()
        # 기간 설정 버튼 누르기
        StartDateBtn = driver.find_element_by_class_name("btn_01")
        StartDateBtn.click()
        time.sleep(0.5)
        # Start / End
        for i in range(2):
            strYear = ''
            strMonth = ''
            strDate = ''

            if i == 0:
                strYear = "2021"
                strMonth = "5"
                strDate = "3"
            else:
                strYear = "2021"
                strMonth = "7"
                strDate = "27"

            # year
            YearBtn = Select(driver.find_elements_by_class_name("ui-datepicker-year")[i])
            YearBtn.select_by_value(strYear)
            time.sleep(0.5)
            #month
            YearBtn = Select(driver.find_elements_by_class_name("ui-datepicker-month")[i])
            YearBtn.select_by_value(strMonth)
            time.sleep(0.5)
            #day
            bIsFind = False
            table = driver.find_elements_by_class_name("ui-datepicker-calendar")[i];
            tbody = table.find_element_by_tag_name("tbody");
            trs = tbody.find_elements_by_tag_name("tr");
            for tr in trs:
                tds = tr.find_elements_by_tag_name("td");
                for td in tds:
                    a = td.find_elements_by_tag_name("a");
                    for a_list in a:
                        if (a_list.text == strDate):
                            a_list.click()
                            bIsFind = True
                            break
                        if bIsFind:break
                    if bIsFind:break
                if bIsFind:break

        # 날짜 적용 후 검색 버튼 클릭.
        Search_Btn = driver.find_element_by_xpath('//*[@id="f_search"]/div/div[2]/div[2]/a[1]')
        Search_Btn.click()
        driver.implicitly_wait(1)

        # 현재 검색 결과의 Page가 몇 장인지 판별하는 함수 필요.
        ResearchResult_div = driver.find_element_by_class_name("paging")
        liResearchResult_a = ResearchResult_div.find_elements_by_tag_name("a")
        Pages_count = len(liResearchResult_a)

        liDateCreated = []
        liTitle = []
        liPrice = []
        liInvestmentOption = []
        liWriter = []
        liSource = []
        liCompanyInfo = []
        liChart = []
        liReportFile = []

        for i in range(Pages_count):
            # 한경 컨센서스 페이지 파싱하기.
            url = driver.current_url

            # ConnectionError방지
            headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/98.0.4758.102" }

            # Request를 사용하여 해당 url을 사용 친화적으로 만든다.
            req = requests.get(url, headers=headers)

            # requests_text 함수를 이용하여 현재 url 정보를 html로 받음
            html = bf(req.content.decode('euc-kr','replace'), "html.parser")

            DataContents = html.find("div", id="contents")
            DataTables = DataContents.find("div", "table_style01")
            tbody = DataTables.find("tbody")
            trs = tbody.find_all("tr")
            for tr in trs:
                tds = tr.find_all("td")
                i = 0
                for td in tds:
                    # 0 : Date
                    if i == 0:
                        liDateCreated.append(td.string)
                    # 1 : title
                    elif i == 1:
                        a = td.find("a")
                        liTitle.append(a.string)
                    # 2 : price
                    elif i == 2:
                        liPrice.append(td.string)
                    # 3 : Opinion
                    elif i == 3:
                        # Pattern 생성
                        word = re.sub(r'\s+', '', td.string)
                        # group() : matching 된 결과 반환
                        if word:
                            liInvestmentOption.append(word)
                        else:
                            print('No match')
                    # 4 : Writer
                    elif i == 4:
                        liWriter.append(td.string)
                    # 5 : Source
                    elif i == 5:
                        liSource.append(td.string)
                    # 6 : CompanyInfo
                    # td안에 div 안에 a 태그안에 있는 링크 주소 담기.
                    elif i == 6:
                        liCompanyInfo.append(td.string)
                    # 7 : Chart
                    elif i == 7:
                        liChart.append(td.string)
                    # 8 : ReportFile
                    elif i == 8:
                        liReportFile.append(td.string)
                    i += 1

            a = 1





