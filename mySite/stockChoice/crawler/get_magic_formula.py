from bs4 import BeautifulSoup
from stockChoice.bizLogic.sorting import Sorting
from stockChoice.utilLibrary.common import Common

# 개별 종목 정보에서 상세 값을 크롤링
def getDetailPrices(tr):
    tdTltle   = tr.find("a", {"class": "tltle"})
    tdsNumber = tr.find_all("td", {"class": "number"})

    companyCode  = tdTltle['href'].replace("/item/main.nhn?code=", "")
    companyName  = tdTltle.text
    presentPrice = tdsNumber[0].text.replace(",", "")
    totalValue   = tdsNumber[6].text.replace(",", "")
    per = tdsNumber[8].text.replace(",", "")
    roa = tdsNumber[9].text.replace(",", "")

    return {"stc_id": companyCode, "stc_name": companyName,
            "now_price": presentPrice, "tot_value": totalValue,
            "per": per, "roa": roa}


# 종목 목록에서 종목정보 검색
# sosok: 0=>코스피, 1=>코스닥
# page : 네이버 조회 목록 페이지
def getPrices(driver):

    bs_obj = BeautifulSoup(driver.page_source, "html.parser")

    # 가격요소 table
    pricesFactorsTable = bs_obj.find("table", {"class": "type_2"})
    pricesFactorsbody  = pricesFactorsTable.find("tbody")
    pricesFactorsTrs   = pricesFactorsbody.find_all("tr", {"onmouseover": "mouseOver(this)"})

    # 결과 Set
    resultSet = []

    for tr in pricesFactorsTrs:
        try:
            resultSet.append(getDetailPrices(tr))
        except:
            print("error: "+tr)

    return resultSet


# 필터링
def filteringData(financeInfoList):
    # 결과 리스트
    resultList = []

    # 반복통한 data 필터링
    for financeInfo in financeInfoList:
        stc_id = financeInfo["stc_id"]
        stc_name = financeInfo["stc_name"]
        now_price = financeInfo["now_price"]
        tot_value = financeInfo["tot_value"]
        per = financeInfo["per"]
        roa = financeInfo["roa"]

        # 조건설정
        if int(tot_value) < 500:
            continue
        if per == "N/A" or roa == "N/A":
            continue
        if float(per) < 0 or float(roa) < 0:
            continue
        resultList.append({'stc_id': stc_id, 'stc_name': stc_name,
                           'now_price': now_price, 'tot_value': tot_value,
                           'per': float(per), 'roa': float(roa)})

    return resultList


###########################################################
# Main 처리: data 읽어서 주식기본 테이블에 저장한다.
###########################################################
def main_process():

    # 전체 data 취합 및 필터링
    totalDataList = []

    # sort instance
    sorting = Sorting()

    #common instance
    commmon = Common()

    # 코스피 driver open
    driver = commmon.set_page_driver("0")

    # 코스피(1, 31+1)
    for pageNum in range(1, 31 + 1):
        click_option = driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/table[2]/tbody/tr/td['+commmon.make_page_num(pageNum)+']/a')
        click_option.click()
        financeInfoList = getPrices(driver)
        totalDataList = totalDataList + filteringData(financeInfoList)

    # 코스피 driver close
    driver.close()

    # 코스닥 driver open
    driver = commmon.set_page_driver("1")

    # 코스닥(1, 28+1)
    for pageNum in range(1, 28 + 1):
        click_option = driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/table[2]/tbody/tr/td['+commmon.make_page_num(pageNum)+']/a')
        click_option.click()
        financeInfoList = getPrices(driver)
        totalDataList = totalDataList + filteringData(financeInfoList)

    # 코스닥 driver close
    driver.close()

    # 전체 파일 리스트를 per 기준 sort
    sortForPer = sorting.sortingListSimpleValue(totalDataList, 'per', False)

    # 전체 파일 리스트를 roa 기준 sort
    sortForPerAndRoa = sorting.sortingListSimpleValue(sortForPer, 'roa', True)

    # per 및 roa 순위 합산 후 sort
    stockList = sorting.sortingListComplexValue(sortForPerAndRoa)

    return stockList
