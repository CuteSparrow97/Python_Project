from Crawling_Finance import Crawling_Finance
from Crawling_News import Crawling_News
from Crawling_Weather import Crawling_Weather
import requests
import json

def test():
    #Crawling_Finace2 = Crawling_Finance()
    #Crawling_Finace2.Search_hankyung('삼성전자')
    m_Crawling_Weather = Crawling_Weather()
    m_Crawling_Weather.SearchWeather("서울시", "강남구", "삼성동")
    # m_Crawling_News = Crawling_News()
    # day, week, month, year # Page
    # lNews = m_Crawling_News.Search_NaverNews('코로나', 'week', 2)
   
def main():
     # 주식 관련 Crawling
    m_Crawling_Finance = Crawling_Finance()
    m_liStockInfo = m_Crawling_Finance.Crawling_PopularStocks()
    m_liKospi = m_Crawling_Finance.Crawling_Kospi()
    m_liKosdaq = m_Crawling_Finance.Crawling_Kosdaq()

    # 주식 출력
    try:
        for StockInfo in m_liStockInfo:
          print (StockInfo)
        print (F'KOSPI : {m_liKospi[0]} / 변화율 : {m_liKospi[1]}({m_liKospi[2]})')
        print (F'KOSDAQ : {m_liKosdaq[0]} / 변화율 : {m_liKosdaq[1]}({m_liKosdaq[2]})')

    except IndexError:
        print("list index out of range(Some list not is not sucessful crawling")

    # 주식 검색
    m_Crawling_Finance.Search_NaverStock("삼성전자")

    # 뉴스 검색
    m_Crawling_News = Crawling_News()
    # day, week, month, year # Page
    lNews = m_Crawling_News.Search_NaverNews('코로나', 'week', 2)

    # Parsing 자료(.csv) POST로 전달하기 위해 준비.
    headers = {'Content-Type' : 'application/json; chearset=utf-8'}
    News_CSV = "C:\\Users\\LCH\Desktop\\test_News.csv"
    Stock_Naver_CSV = "C:\\Users\\LCH\Desktop\\test_Stock_Naver.csv"
    Stock_HK_CSV = "C:\\Users\\LCH\Desktop\\test_Stock_HK.csv"
    News_file = {'upload_file' : open(News_CSV, 'r', encoding='utf-8')}
    Stock_Naver = {'upload_file' : open(Stock_Naver_CSV, 'r', encoding='utf-8')}
    Stock_HK = {'upload_file' : open(Stock_HK_CSV, 'r', encoding='utf-8')}

    # POST
    data = {'NEWS' : lNews, 'KOSPI' : m_liKospi, 'KOSDAQ' : m_liKosdaq, 'News' : News_file,
    'Stock_HK' : Stock_HK, 'Stock_Naver' : Stock_Naver}
    res = requests.post('http://benefit.run.goorm.io/api/v1/weather', data = json.dumps(data, default=list, indent="\t"), headers = headers)
    print(str(res.status_code) + " | " + res.text)

if __name__ == "__main__":
    #main()
    test()
