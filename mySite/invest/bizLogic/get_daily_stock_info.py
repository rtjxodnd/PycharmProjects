# https://finance.naver.com 으로부터 일별 종가정보를 크롤링한다.
# 읽어들인 정보를 DB에 저장한다.
# pgmId = STC0002
# Creator = 서태웅
# History
# 20190204 신규 생성
# 20190329 postgre에서 mySql로 변경
# 20190329 로깅 모듈 추가
# 20190520 Django에 삽입

# 필요라이브러리 import
from invest.models import Stc001, Stc002
import datetime as dt
import requests
from bs4 import BeautifulSoup
import logging

# 로거
logger = logging.getLogger(__name__)

# 공통변수
FINANCE_URL = "https://finance.naver.com/item/sise_day.nhn?code="

# 결과건수 초기화
g_insert_quantity_stock = 0
g_insert_quantity_daily_info = 0

# 한페이지의 data 추출
# page: 웹 페이지 지정
def find_stock_values_of_one_page(stock_id, input_dt, page=1):
    try:
        # 데이터 탐색
        url = FINANCE_URL+stock_id+"&page="+str(page)
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
        trs = bs_obj.find_all("tr", {"onmouseover": "mouseOver(this)"})

        # 해당 page 의 last order 구하기(보통 한페이지당 10개의 일자 데이터가 있다. 그러나 마지막 데이터는 그보다 적음)
        last_order = -1
        for order in range(0, 10):
            tr = trs[order]
            tds = tr.find_all("td", {"align": "center"})
            if len(tds[0].text.replace(".", "").replace(" ", "")) == 0:
                break
            last_order = last_order + 1

        # 필요 데이터 추출
        for order in range(last_order, -1, -1):
            tr = trs[order]
            tds = tr.find_all("td")
            result_one_value = find_stock_values_of_one(stock_id, input_dt,tds)
            result_one_value["stock_id"] = stock_id
            result_one_value["page"] = page
            result_page_value = result_one_value

        # return
        return result_page_value

    except IndexError:
        # 페이지의 끝
        result_page_value = {"endOfData": "Y",
                             "stock_id": stock_id,
                             "page": page}

        # return
        return result_page_value

    except Exception as ex:
        logger.error("ERROR!!!!: find_stock_values_of_one_page")
        logger.error(ex)


# 한건의 data 추출
# tds: 입력된 tds data
# stockOrder: 해당 페이지 내에서의 순서
def find_stock_values_of_one(stock_id, input_dt, tds):
    try:
        # 필요 데이터 추출
        # 상승하락여부 추출
        up_and_down = "1"
        if tds[2].find("img") is not None:
            up_and_down = tds[2].find("img").get('src').split("_")[1][:2].replace("up", "1").replace("do", "-1")  # 상승하락

        # 일자추출
        base_dt = tds[0].find("span").text.replace(".", "")  # 기준일
        # 나머지 세팅
        result_value = { "endOfData": "N",
                       "baseDt": base_dt,
                       "stock_id": stock_id, #종목ID
                       "clsPrice": tds[1].find("span").text.replace(",", ""),  # 금일종가
                       "sign": up_and_down,  # 상승하락
                       "diffPrice": tds[2].find("span").text.replace("	", "").replace("\n", "").replace(",", ""),  # 변동금액
                       "strtPrice": tds[3].text.replace(",", ""),  #시가
                       "highPrice": tds[4].text.replace(",", ""),  #고가
                       "lowPrice": tds[5].text.replace(",", ""),  # 저가
                       "dealQnt": tds[6].text.replace(",", "")}  # 거래량

        # db 입력
        if input_dt <= base_dt:
            stock_values_insert_to_db(result_value)

        # return
        return result_value

    except IndexError:
        # 페이지의 끝
        result_value = {"endOfData": "Y"}

        # return
        return result_value

    except Exception as ex:
        logger.error("ERROR!!!!: find_stock_values_of_one")
        logger.error(ex)


# 입력된 dictionary 를 db insert
def stock_values_insert_to_db(insert_value):
    # 입력정보 parsing
    base_dt = insert_value['baseDt']
    stc_id = insert_value['stock_id']
    mod_cls_price = 0
    cls_price = insert_value['clsPrice']
    diff_price = float(insert_value['sign']) * float(insert_value['diffPrice'])
    strt_price = insert_value['strtPrice']
    high_price = insert_value['highPrice']
    low_price = insert_value['lowPrice']
    deal_qnt = insert_value['dealQnt']
    pgm_id = "STC0002"

    # data 별 DB insert
    try:
        id = Stc002.objects.get(stc_id=stc_id, base_dt=base_dt).id
        insert_data = Stc002.objects.get(id=id)
        insert_data.mod_cls_price = mod_cls_price
        insert_data.cls_price = cls_price
        insert_data.diff_price = diff_price
        insert_data.strt_price = strt_price
        insert_data.high_price = high_price
        insert_data.low_price = low_price
        insert_data.deal_qnt = deal_qnt
        insert_data.pgm_id = pgm_id
        insert_data.save()
        return
    except Stc002.DoesNotExist as de:
        insert_data = Stc002(stc_id=stc_id,
                             base_dt=base_dt,
                             mod_cls_price=mod_cls_price,
                             cls_price=cls_price,
                             diff_price=diff_price,
                             strt_price=strt_price,
                             high_price=high_price,
                             low_price=low_price,
                             deal_qnt=deal_qnt,
                             pgm_id=pgm_id)
        insert_data.save()
        g_insert_quantity_daily_info += 1
        return
    except Exception as ex:
        error_result_dict = { "base_dt": insert_value['baseDt'],
                              "companyCode": insert_value['stock_id']}

        logger.error("ERROR!!!!: stock_values_insert_to_db")
        logger.error(error_result_dict)
        logger.error(ex)


# 해당 종목의 마지막 page 추출
def get_last_page_of_stock (stc_id, input_dt):
    url = FINANCE_URL+stc_id
    page_call_result = requests.get(url)
    bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
    td_pg_rr = bs_obj.find("td",{"class": "pgRR"})

    # 마지막 페이지가 가리키는 위치 확인
    # 마지막 페이지 링크버튼 없다면 해당 종목은 1개의 페이지만 존재한다.
    if td_pg_rr is None:
        last_page = 1
    else:
        href = td_pg_rr.find("a")["href"]
        last_page = int(href.split("=")[2])

    # 입력된 일자가 어떤 페이지에 포함되는지 확인한다.
    set_yn = "N"
    for page in range(0, last_page):
        url = url+"&page="+str(page + 1)
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
        day_tds = bs_obj.find_all("td", {"align": "center"})

        for day_td in day_tds:
            day = day_td.find("span", {"class": "tah p10 gray03"})
            if input_dt >= day.text.replace(".", ""):
                last_page = page + 1
                set_yn = "Y"
                break

        if set_yn == "Y":
            break

    # 대략 2010초 언저리: 225 page, 2010년 이후 데이터만 저장
    if last_page > 225:
        last_page = 225

    return last_page


# 한개 종목에 대한 전체처리
def insert_daily_cls_price(stc_id, input_dt):
    for page in range(get_last_page_of_stock(stc_id, input_dt), 0, -1):
        find_stock_values_of_one_page(stc_id, input_dt, page)


###########################################################
# Main 처리: 주식 기본 테이블에서 data 읽어서 이를 처리한다.
###########################################################
def main_process(input_dt=dt.datetime.today().strftime("%Y%m%d")):

    # 조회수행
    # 입력된 일자보다 크거나 같으면서 Stc001에 종목정보가 있는 data 중 일별정보가 없는 data
    # 입력된 일자에 해당하는 data 수신
    sql_select = "SELECT a.stc_id FROM rtjxodnd.stc001 a "\
                 "  LEFT JOIN(SELECT stc_id FROM rtjxodnd.stc002 WHERE base_dt >= %s) b"\
                 " USING (stc_id)"\
                 " WHERE b.stc_id IS NULL"\
                 " UNION" \
                 " SELECT a.stc_id FROM rtjxodnd.stc001 a " \
                 "  LEFT JOIN(select stc_id from rtjxodnd.stc002 where base_dt = %s) b"\
                 " USING(stc_id);"
    Stc001.objects.raw(sql_select, input_dt, input_dt)
    selected_rows = Stc001.objects.all()

    # 데이타 Fetch
    for row in selected_rows:
        try:
            insert_daily_cls_price(row.stc_id, input_dt)

        except Exception as ex:
            logger.error("ERROR!!!!: main_process")
            logger.error(ex)

    return {'insert_quantity_stock': g_insert_quantity_stock}


if __name__ == "__main__":
    main_process('20190625')
