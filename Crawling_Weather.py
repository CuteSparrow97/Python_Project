import re
from datetime import datetime
import pandas as pd
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

class Crawling_Weather():
    def SearchWeather(self, strCity, strAddr1, strAddr2):
        self.strCity = strCity
        self.strAddr1 = strAddr1
        self.strAddr2 = strAddr2

    # Selenium Option 설정
        Selenium_Option = webdriver.ChromeOptions()
        Selenium_Option.add_argument('headless')    # 창 안뜨게 함.
        Selenium_Option.add_argument('window-size=1920x1080')   # 창 크기 조절
        Selenium_Option.add_argument('disable-gpu')

        # Chromedriver 가져오기.
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.implicitly_wait(3)

        # Chrome Driver 실행
        driver.get('https://www.naver.com/')
        driver.implicitly_wait(1)

        # 텍스트 창 가져오기
        strAddr = strCity + " " + strAddr1 + " " + strAddr2 + " 날씨"
        TextInput = driver.find_element_by_class_name("input_text")
        TextInput.send_keys(strAddr)
        TextInput.submit()
        driver.implicitly_wait(1)

        liHour = []         # 시각
        liWeather = []      # 날씨
        liTemperature = []  # 온도
        liHumidity = []     # 습도
        liWind = []         # 바람

        # 현재 시각 가져오기
        now = datetime.now()
        nHour = now.hour
        strHour = ""
        if (nHour < 10):
            strHour = "0"+ str(nHour) + "시"
        else:
            strHour = nHour + "시"
        liHour.append(strHour)

        # 현재 온도 가져오기


        # 현재 시각 날씨 (현재 시각이 몇시인지 안나와있음)
        strNowWeather = driver.find_element_by_class_name("weather_main").find_elements_by_class_name("blind")[0].text
        liWeather.append(strNowWeather)
        print(strNowWeather)

        # 현재 시각 습도
        divInformation = driver.find_element_by_class_name("temperature_info")
        dts = divInformation.find_elements_by_tag_name("dt")
        dds = divInformation.find_elements_by_tag_name("dd")
        strNowHumidity = ""
        strNowWind = ""

        nIndex = 0
        for dt in dts:
            ntitle = dt.text
            if ("습도" in ntitle):
                strNowHumidity = dds[nIndex].text
            elif ("바람" in ntitle):
                strNowWind = dds[nIndex].text
                
            nIndex +=1

        print(strNowHumidity)
        print(strNowWind)

        # 시간대 별 날씨 파싱
        divWeather_hourly = driver.find_element_by_xpath('//*[@id="main_pack"]/section[1]/div[1]/div[2]/div[1]/div[2]/div/div/div[2]/div/div/div/div[2]')
        ul = divWeather_hourly.find_element_by_tag_name("ul")
        lis = ul.find_elements_by_tag_name("li")
        
        for li in lis:
            strDay_Attr = li.get_attribute("data-day")
            if strDay_Attr == "tomorrow":
                break;

            # 시간대 파싱
            strHourly = li.text
            re_1 = re.compile('^(\w{2}\D)')
            word = re_1.search(strHourly)
            strHour = word.group()
            liHour.append(strHour)

            # 날씨 파싱
            re_1 = re.compile('\D\D(?=\\n)')
            word = re_1.search(strHourly)
            strWeather = word.group()
            liWeather.append(strWeather)

            b = 3

        print(liHour)
        print(liWeather)
        a = 2
        # 시간대 별 강수 파싱

        # 시간대 별 바람 파싱

        # 시간대 별 습도 파싱

        Weather_df = pd.DataFrame({'Hour':liHour,'Weather': liWeather})
        Weather_df.to_csv("C:\\Users\\LCH\Desktop\\test_Weather.csv",",","NaN", index=False, encoding='utf-8-sig')
        #Stock_HK_df.to_csv("C:\\Users\\dlckd\Desktop\\test1.csv",",","NaN", index=False, encoding='utf-8-sig')