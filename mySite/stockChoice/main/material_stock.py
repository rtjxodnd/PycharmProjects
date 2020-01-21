from invest.models import Stc001
from stockChoice.crawler import get_material_stock as crawler


# 평균값 산출
def calculator_avg(factors):
    # 초기값 설정
    tot_sum = 0  # 피제수설정
    j = 0  # 제수설정

    # 숫자 변환 및 제수 절정
    for i in factors:
        if factors[i] == "\xa0" or factors[i] == "-" or factors[i] == "":
            factors[i] = 0
        else:
            factors[i] = float(factors[i].replace(",", ""))
            j += 1

    # 합계값
    for i in factors:
        # 과거 데이터 중 하나라도 음수 있으면 0 리턴하고 종료.
        tot_sum += factors[i]

    # 제수가 0이면 roe = 0 리턴
    if j == 0:
        return {"avg": 0}

    # 평균값 계산
    avg = tot_sum / j

    return {"avg": avg}


# 음수검증
def calculator_recent(factors):
    # 숫자 변환 및 제수 절정
    for i in factors:
        if factors[i] == "\xa0" or factors[i] == "-" or factors[i] == "":
            factors[i] = 0
        else:
            factors[i] = float(factors[i].replace(",", ""))

        # 하나라도 음수 있으면 -1 리턴하고 종료.
        if factors[i] < 0:
            return {"recent": -1}

    return {"recent": 1}

###########################################################
# Main 처리: data 읽어서 필터링한다.
###########################################################
def main_process(goal_profit = 15):
    # 결과리스트
    resultList = []

    # 전체 종옥목록
    last_digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    stockList = Stc001.objects.filter(face_price__gt=0, tot_value__lte=70000000000, tot_value__gte=25000000000)
    # stockList = Stc001.objects.filter(face_price__gt=0)
    # stockList = Stc001.objects.filter(face_price__gt=0, stc_id='005930') #28513K, 317770
    # stockList = Stc001.objects.filter(face_price__gt=0, id__lt=10)

    # 전체 종목 대상
    for stock in stockList:

        try:
            # data추출
            crawling_data = crawler.find_one_stock_values(stock.stc_id)
            price_high_52week = crawling_data["price_high_52week"]
            price_low_52week = crawling_data["price_low_52week"]
            sales_accounts = crawling_data["sales_accounts"]
            operating_profits = crawling_data["operating_profits"]
            net_incomes = crawling_data["net_incomes"]
            op_margins = crawling_data["op_margins"]
            net_margins = crawling_data["net_margins"]
            roes = crawling_data["roes"]
            debt_ratios = crawling_data["debt_ratios"]
            quick_ratios = crawling_data["quick_ratios"]
            reservation_rate = crawling_data["reservation_rates"]
            sales_accounts_recent = crawling_data["sales_accounts_recent"]
            operating_profits_recent = crawling_data["operating_profits_recent"]
            net_incomes_recent = crawling_data["net_incomes_recent"]
            op_margins_recent = crawling_data["op_margins_recent"]
            net_margins_recent = crawling_data["net_margins_recent"]
            roes_recent = crawling_data["roes_recent"]
            debt_ratios_recent = crawling_data["debt_ratios_recent"]
            quick_ratios_recent = crawling_data["quick_ratios_recent"]
            reservation_rate_recent = crawling_data["reservation_rates_recent"]

            # 평균값 산출
            avg_sales_account = calculator_avg(sales_accounts)["avg"]
            avg_operating_profit = calculator_avg(operating_profits)["avg"]
            avg_net_income = calculator_avg(net_incomes)["avg"]
            avg_op_margin = calculator_avg(op_margins)["avg"]
            avg_net_margin = calculator_avg(net_margins)["avg"]
            avg_roe = calculator_avg(roes)["avg"]
            avg_debt_ratios = calculator_avg(debt_ratios)["avg"]
            avg_quick_ratios = calculator_avg(quick_ratios)["avg"]
            avg_reservation_rate = calculator_avg(reservation_rate)["avg"]

            # 음수검증
            sales_account_recent = calculator_recent(sales_accounts_recent)["recent"]
            operating_profit_recent = calculator_recent(operating_profits_recent)["recent"]
            net_income_recent = calculator_recent(net_incomes_recent)["recent"]
            op_margin_recent = calculator_recent(op_margins_recent)["recent"]
            net_margin_recent = calculator_recent(net_margins_recent)["recent"]
            roe_recent = calculator_recent(roes_recent)["recent"]

            # output
            if stock.stc_dvsn == '01':
                stc_dvsn = '코스피'
            else:
                stc_dvsn = '코스닥'

            # 판단
            sell_yn = True

            # 현재가의 1.5배가 52주 최고가가 보다 크면 매수 안함
            if float(stock.now_price)*1.5 > float(price_high_52week):
                sell_yn = False
            print("1", sell_yn)
            # 매출액 평균이 0보다 작으면 매수 안함
            if avg_sales_account < 0:
                sell_yn = False
            print("2", sell_yn)
            # 영업이익 평균이 0보다 작으면 매수 안함
            if avg_operating_profit < 0:
                sell_yn = False
            print("3", sell_yn)
            # 당기순이익 평균이 0보다 작으면 매수 안함(조건삭제)
            # if avg_net_income < 0:
            #     sell_yn = False
            print("4", sell_yn)
            # 영업이익률 평균이 0보다 작으면 매수 안함
            if avg_op_margin < 0:
                sell_yn = False
            print("5", sell_yn)
            # 순이익률 평균이 0보다 작으면 매수 안함
            if avg_net_margin < 0:
                sell_yn = False
            print("6", sell_yn)
            # ROE 평균이 0보다 작으면 매수 안함
            if avg_roe < 0:
                sell_yn = False
            print("7", sell_yn)
            # 최근 매출액 중 음수가 있으면 매수 안함
            if sales_account_recent < 0:
                sell_yn = False
            print("8", sell_yn)
            # 최근 영업이익 중 음수가 있으면 매수 안함
            if operating_profit_recent < 0:
                sell_yn = False
            print("9", sell_yn)
            # 최근 당기순이익 중 음수가 있으면 매수 안함(조건삭제)
            # if net_income_recent < 0:
            #     sell_yn = False
            print("10", sell_yn)
            # 최근 영업이익률 중 음수가 있으면 매수 안함
            if op_margin_recent < 0:
                sell_yn = False
            print("11", sell_yn)
            # 최근 순이익률 중 음수가 있으면 매수 안함(조건삭제)
            # if net_margin_recent < 0:
            #     sell_yn = False
            print("12", sell_yn)
            # 최근 ROE 중 음수가 있으면 매수 안함
            if roe_recent < 0:
                sell_yn = False
            print("13", sell_yn)
            # 거래금액이 2000000000보다 크면 매수 안함
            if stock.deal_amt > 5000000000:
                sell_yn = False
            print("14", sell_yn)
            # 부채율이 150보다 크면 매수 안함
            if avg_debt_ratios > 150:
                sell_yn = False
            print("14", sell_yn)

            # 매수여부
            if sell_yn:
                judge_context = "매수고려"
            else:
                judge_context = "매수불가"

            # 매수 여뷰 Y 것 만 결과 세팅
            if sell_yn:
                resultList.append({"stc_id": stock.stc_id,
                                   "stc_name": stock.stc_name,
                                   "stc_dvsn": stc_dvsn,
                                   "price": float(stock.now_price),
                                   "price_high_52week": float(price_high_52week),
                                   "price_low_52week": float(price_low_52week),
                                   "avg_sales_account": round(avg_sales_account, 2),
                                   "avg_operating_profit": round(avg_operating_profit, 2),
                                   "avg_net_income": round(avg_net_income, 2),
                                   "avg_op_margin": round(avg_op_margin, 2),
                                   "avg_net_margin": round(avg_net_margin, 2),
                                   "avg_debt_ratios": round(avg_debt_ratios, 2),
                                   "avg_quick_ratios": round(avg_quick_ratios, 2),
                                   "avg_reservation_rate": round(avg_reservation_rate, 2),
                                   "avg_roe": round(avg_roe, 2),
                                   "deal_amt": round(stock.deal_amt, 2),
                                   "judge_context": judge_context})

        except Exception as e:
            print(stock.stc_id)
            print(e)

    return resultList
