from asyncio.windows_events import NULL
from typing import Text
import requests
import os
import time
import re
import pandas as pd
from selenium import webdriver
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup as bf
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




        a = 1