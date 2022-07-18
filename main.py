from Crawling_Finance import Crawling_Finance
from Crawling_News import Crawling_News
import requests
import json

def test():
    # 뉴스 검색
    m_Crawling_News = Crawling_News()
    # day, week, month, year
    lNews = m_Crawling_News.Search_NaverNews('코로나', 'week')
   
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
    m_Crawling_Finance.Search_StockandCrawling("삼성전자")

    # 뉴스 검색
    m_Crawling_News2 = Crawling_News2()
    lNews = m_Crawling_News2.Search_NaverNews("십자매")

    # POST
    headers = {'Content-Type' : 'application/json; chearset=utf-8'}
    csv_file = "C:\\Users\\LCH\Desktop\\test1.csv"
    files = {'upload_file' : open(csv_file, 'r', encoding='utf-8')}
    data = {'NEWS' : lNews, 'KOSPI' : m_liKospi, 'KOSDAQ' : m_liKosdaq, 'files' : files}
    # res = requests.post('http://benefit.run.goorm.io/api/v1/weather', data = json.dumps(data), headers = headers)
    res = requests.post('http://benefit.run.goorm.io/api/v1/weather', data = json.dumps(data, default=list, indent="\t"), headers = headers)
    print(str(res.status_code) + " | " + res.text)

if __name__ == "__main__":
    #main()
    test()
