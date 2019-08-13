# https://finance.naver.com 으로부터 종목 기본정보를 크롤링한다.
# 읽어들인 정보를 DB에 저장한다.
# pgm_id = STC0003
# Creator = 서태웅
# History
# 20190721 신규 생성


# 필요라이브러리 import
from invest.models import Stc003
import datetime as dt
from bs4 import BeautifulSoup
import logging
from selenium import webdriver
from config import config
chromeDriverPath = config.chromeDriverPath()

# 로거
logger = logging.getLogger(__name__)


# 한건의 data 추출
# sosok: 0코스닥, 1코스피
# page: 웹 페이지 지정
# stockOrder: 해당 페이지 내에서의 순서
def find_one_page_stock_values(driver):
    try:
        result_num = 0

        # 데이터 탐색
        bs_obj = BeautifulSoup(driver.page_source, "html.parser")

        # 가격요소 table
        pricesFactorsTable = bs_obj.find("table", {"class": "type_2"})
        pricesFactorsbody = pricesFactorsTable.find("tbody")
        pricesFactorsTrs = pricesFactorsbody.find_all("tr", {"onmouseover": "mouseOver(this)"})

        # 개별행 탐색
        for tr in pricesFactorsTrs:

            # 1개 행 추출
            tds = tr.find_all("td")

            # 필요 데이터 추출
            result_value = {"stcId": tds[1].find("a").get('href')[-6:],
                            "per": tds[6].text.replace(",", ""),
                            "roe": tds[7].text.replace(",", ""),
                            "roa": tds[8].text.replace(",", ""),
                            "pbr": tds[9].text.replace(",", "")}

            # db 입력
            result_num += stock_values_insert_to_db(result_value)

        # return
        return result_num

    except Exception as ex:
        print(tr)
        logger.error("ERROR!!!!: find_one_stock_values")
        logger.error(ex)


# 입력된 dictionary 를 db insert
# insert_value: 입력된 dictionary 형태의 종목정보
def stock_values_insert_to_db(insert_value):
    stc_id = insert_value['stcId']
    base_dt = dt.datetime.today().strftime("%Y%m%d")
    pbr = float(insert_value['pbr'].replace("N/A", "0"))
    per = float(insert_value['per'].replace("N/A", "0"))
    roe = float(insert_value['roe'].replace("N/A", "0"))
    roa = float(insert_value['roa'].replace("N/A", "0"))

    try:
        id = Stc003.objects.get(stc_id=stc_id, base_dt=base_dt).id
        insert_data = Stc003.objects.get(id=id)
        insert_data.pbr = pbr
        insert_data.per = per
        insert_data.roe = roe
        insert_data.roa = roa
        insert_data.pgm_id = 'STC0003'
        insert_data.save()
        return 1

    except Stc003.DoesNotExist as de:
        insert_data = Stc003(stc_id=stc_id,
                             base_dt=base_dt,
                             pbr=pbr,
                             per=per,
                             roe=roe,
                             roa=roa,
                             pgm_id='STC0003')
        insert_data.save()
        return 1

    except Exception as ex:
        logger.error(insert_value)
        logger.error("ERROR!!!!: stock_values_insert_to_db")
        logger.error(ex)
        return 0


###########################################################
# page driver 설정
###########################################################
def set_page_driver(sosok):
    # driver = webdriver.Chrome(chromeDriverPath)
    driver = webdriver.Chrome()
    url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok="+sosok
    driver.get(url)
    click_option1 = driver.find_element_by_xpath("//*[@id='option1']")
    click_option2 = driver.find_element_by_xpath("//*[@id='option4']")
    click_option3 = driver.find_element_by_xpath("//*[@id='option15']")
    click_option4 = driver.find_element_by_xpath("//*[@id='option18']")
    click_option5 = driver.find_element_by_xpath("//*[@id='option21']")
    click_option6 = driver.find_element_by_xpath("//*[@id='option24']")
    click_option7 = driver.find_element_by_xpath('//*[@id="contentarea_left"]/div[2]/form/div/div/div/a[1]/img')
    click_option1.click()
    click_option2.click()
    click_option3.click()
    click_option4.click()
    click_option5.click()
    click_option6.click()
    click_option7.click()

    return driver


###########################################################
# pageNum 보정
###########################################################
def make_page_num(pageNum):
    if pageNum < 3:
        pageNum = str(pageNum)
    elif pageNum < 12:
        pageNum = str(pageNum + 1)
    else:
        pageNum = str(((pageNum - 2) % 10) + 4)
    return pageNum


###########################################################
# Main 처리: data 읽어서 주식일별내역 테이블에 저장한다.
###########################################################
def main_process():
    # 결과건수 초기화
    insert_quantity_kospi = 0
    insert_quantity_kosdaq = 0

    # 코스피 driver open
    driver = set_page_driver("0")

    # 코스피(1, 31+1)
    for pageNum in range(1, 31 + 1):
        click_option = driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/table[2]/tbody/tr/td['+make_page_num(pageNum)+']/a')
        click_option.click()
        insert_quantity_kospi += find_one_page_stock_values(driver)

    # 코스피 driver close
    driver.close()

    # 코스닥 driver open
    driver = set_page_driver("1")

    # 코스닥(1, 28+1)
    for pageNum in range(1, 28 + 1):
        click_option = driver.find_element_by_xpath('//*[@id="contentarea"]/div[3]/table[2]/tbody/tr/td['+make_page_num(pageNum)+']/a')
        click_option.click()
        insert_quantity_kosdaq += find_one_page_stock_values(driver)

    # 코스닥 driver close
    driver.close()

    return {'insert_quantity_kospi': insert_quantity_kospi,
            "insert_quantity_kosdaq": insert_quantity_kosdaq}