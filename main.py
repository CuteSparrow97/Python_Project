from Crawling_Finance import Crawling_Finance

def test():
    m_Crawling_Finance = Crawling_Finance()
    m_Crawling_Finance.Search_StockandCrawling("삼성전자")

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


if __name__ == "__main__":
    #main()
    test()