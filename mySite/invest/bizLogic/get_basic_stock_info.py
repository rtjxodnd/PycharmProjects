# https://finance.naver.com 으로부터 종목 기본정보를 크롤링한다.
# 읽어들인 정보를 DB에 저장한다.
# pgm_id = STC0001
# Creator = 서태웅
# History
# 20190126 신규 생성
# 20190210 insert 문을 update insert 로 수정
# 20190328 postgre에서 mySql로 변경
# 20190329 로깅 모듈 추가
# 20190520 Django에 삽입


# 필요라이브러리 import
from invest.models import Stc001
import requests
from bs4 import BeautifulSoup
import logging

# 로거
logger = logging.getLogger(__name__)


# 한건의 data 추출
# sosok: 0코스닥, 1코스피
# page: 웹 페이지 지정
# stockOrder: 해당 페이지 내에서의 순서
def find_one_stock_values(sosok=0, page=1, stockOrder=0):
    try:
        # 데이터 탐색
        url = "https://finance.naver.com/sise/sise_market_sum.nhn?sosok="+str(sosok)+"&page="+str(page)
        page_call_result = requests.get(url)
        bs_obj = BeautifulSoup(page_call_result.content, "html.parser")
        tbody  = bs_obj.find("tbody")
        trs    = tbody.find_all("tr", {"onmouseover": "mouseOver(this)"})
        tr     = trs[stockOrder]
        tds    = tr.find_all("td")

        # 주식구분 설정
        if sosok == 0:
            stc_dvsn = "01"
        elif sosok == 1:
            stc_dvsn = "02"
        else:
            stc_dvsn = "03"

        # 필요 데이터 추출
        result_value = { "endOfData": "N",
                       "sosok": sosok,
                       "page": page,
                       "stockOrder": stockOrder,
                       "stcId": tds[1].find("a").get('href')[-6:], # 종목코드
                       "stcNm": tds[1].find("a").text,             # 종목명
                       "stcDvsn": stc_dvsn,
                       "nowPrice": tds[2].text.replace(",", ""),    #현재가
                       "facePrice": tds[5].text.replace(",", ""),  #액면가
                       "totValue": float(tds[6].text.replace(",", "")) * 1000000000}  # 시가총액

        # db 입력
        stock_values_insert_to_db(result_value)

        # return
        return result_value

    except IndexError:
        # 페이지의 끝
        result_value = {"endOfData": "Y",
                        "sosok": sosok,
                        "page": page,
                        "stockOrder": stockOrder}

        # return
        return result_value

    except Exception as ex:
        logger.error("ERROR!!!!: find_one_stock_values")
        logger.error(ex)


# 기존 data delete
def stock_values_delete(kospi_yn="N", kosdaq_yn="N"):
    try:
        if kospi_yn == "Y":
            query = Stc001.objects.filter(stc_dvsn='01')
            query.delete()

        if kosdaq_yn == "Y":
            query = Stc001.objects.filter(stc_dvsn='02')
            query.delete()

        return
    except Exception as ex:
        logger.error("ERROR!!!!: stock_values_delete")
        logger.error(ex)


# 입력된 dictionary 를 db insert
# insert_value: 입력된 dictionary 형태의 종목정보
def stock_values_insert_to_db(insert_value):
    stc_id = insert_value['stcId']
    stc_name = insert_value['stcNm']
    stc_dvsn = insert_value['stcDvsn']
    now_price = insert_value['nowPrice']
    face_price = insert_value['facePrice']
    tot_value = insert_value['totValue']
    pgm_id = "STC0001"
    try:
        id = Stc001.objects.get(stc_id=stc_id).id
        insert_data = Stc001.objects.get(id=id)
        insert_data.stc_name = stc_name
        insert_data.stc_dvsn = stc_dvsn
        insert_data.now_price = now_price
        insert_data.face_price = face_price
        insert_data.tot_value = tot_value
        insert_data.pgm_id = pgm_id
        insert_data.save()
        return
    except Stc001.DoesNotExist as de:
        insert_data = Stc001(stc_id=stc_id,
                             stc_name=stc_name,
                             stc_dvsn=stc_dvsn,
                             now_price=now_price,
                             face_price=face_price,
                             tot_value=tot_value,
                             pgm_id=pgm_id)
        insert_data.save()
        return
    except Exception as ex:
        error_result_dict = { "companyCode": insert_value['stcId']
                            , "sosok": insert_value['sosok']
                            , "page": insert_value['page']
                            , "stockOrder": insert_value['stockOrder']}
        logger.error(error_result_dict)
        logger.error("ERROR!!!!: stock_values_insert_to_db")
        logger.error(ex)


###########################################################
# Main 처리: 주식 기본 테이블삭제 후 data 읽어서 주식기본 테이블에 저장한다.
###########################################################
def main_process(kospi_yn="N", kosdaq_yn="N"):

    # 시간 check
    # cur_time = time.strftime("%H%M%S")
    # if cur_time < '090000':
    #     logger.error("ERROR!!!!: main_process")
    #     logger.error("09시 이전 처리 불가")
    #     raise myError.TimeCheckError

    # 결과건수 초기화
    insert_quantity_kospi = 0
    insert_quantity_kosdaq = 0

    # 코스피자료 수신
    if kospi_yn == "Y":
        # 코스피 전체 추출
        # 코스피(소속=0, 전체 페이지=31)
        sosok = 0
        tot_pages = 31 + 1
        for page in range(1, tot_pages):
            # 한페이지의 data 추출
            for stockOrder in range(0, 50):
                if find_one_stock_values(sosok, page, stockOrder)['endOfData'] == 'Y':
                    logger.error("kospi data 끝")
                    break
                else:
                    insert_quantity_kospi += 1

    # 코스닥 자료 수신
    if kosdaq_yn == "Y":
        # 코스닥 전체 추출
        # 코스닥(소속=1, 전체 페이지=28)
        sosok = 1
        tot_pages = 28 + 1
        for page in range(1, tot_pages):
            # 한페이지의 data 추출
            for stockOrder in range(0, 50):
                if find_one_stock_values(sosok, page, stockOrder)['endOfData'] == 'Y':
                    logger.error("kosdaq data 끝")
                    break
                else:
                    insert_quantity_kosdaq += 1

    return {'insert_quantity_kospi': insert_quantity_kospi,
            "insert_quantity_kosdaq": insert_quantity_kosdaq}


if __name__ == "__main__":
    main_process(kospi_yn="Y", kosdaq_yn="Y")

