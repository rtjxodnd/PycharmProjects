from invest.models import Stc001
from stockChoice.crawler import get_bond_style_stock as crawler


# 예상 평균 roe 산출
def calculator_avg_roe(roes):
    # 초기값 설정
    sum_roe = 0  # 피제수설정
    j = 0  # 제수설정

    # 숫자 변환 및 제수 절정
    for i in roes:
        if roes[i] == "N/A":
            roes[i] = 0
        else:
            roes[i] = float(roes[i].replace(",", ""))
            j += 1

    # 평균값 계산
    for i in roes:
        # # 과거 데이터 중 하나라도 음수 있으면 0 리턴하고 종료.
        # if roes[i] < 0:
        #     return {"avg_roe": 0, "standard_deviation": 0}
        # # 정상적 값일경우 합더하기
        # elif roes[i] >= 0:
        #     sum_roe += roes[i]
        sum_roe += roes[i]
    # 제수가 0이면 roe = 0 리턴
    if j == 0:
        return {"avg_roe": 0, "standard_deviation": 0}

    avg_roe = sum_roe / j

    # 표준편차 계산
    sum_diff = 0
    for i in roes:
        if roes[i] != 0:
            diff = roes[i] - avg_roe
            sum_diff = sum_diff + pow(diff, 2)

    dispersion = sum_diff / j
    standard_deviation = pow(dispersion, 0.5)

    # 보정계수 계산
    # 최근 제외 11개 데이타를 3,4,4 개로 나누고 3그룹간 평균 비교
    avg_group1 = (roes["roe1"] + roes["roe2"] + roes["roe3"]) / 3
    avg_group2 = (roes["roe4"] + roes["roe5"] + roes["roe6"] + roes["roe7"]) / 4
    avg_group3 = (roes["roe8"] + roes["roe9"] + roes["roe10"] + roes["roe11"]) / 4

    correction_factor = 0

    # 지속상승
    if (avg_group1 >= avg_group2) & (avg_group2 >= avg_group3):
        correction_factor = 1.1
    # 하락 후 상승
    elif (avg_group1 >= avg_group2) & (avg_group2 <= avg_group3):
        correction_factor = 1.05
    # 상승 후 하락
    elif (avg_group1 <= avg_group2) & (avg_group2 >= avg_group3):
        correction_factor = 0.9
    # 지속하락
    elif (avg_group1 <= avg_group2) & (avg_group2 <= avg_group3):
        correction_factor = 0.8

    return {"avg_roe": avg_roe * correction_factor, "standard_deviation": standard_deviation}


# 예상 평균 배당률 산출
def calculator_avg_dis(diss):
    # 초기값 설정
    sum_dis = 0  # 피제수설정
    j = 0  # 제수설정

    # 숫자 변환 및 제수 절정
    for i in diss:
        if diss[i] == "N/A":
            diss[i] = 0
        else:
            diss[i] = float(diss[i].replace(",", ""))
            j += 1

    # 평균값 계산
    for i in diss:
        sum_dis += diss[i]

    # 제수가 0이면 roe = 0 리턴
    if j == 0:
        return 0

    avg_dis = sum_dis / j

    return avg_dis

###########################################################
# Main 처리: data 읽어서 필터링한다.
###########################################################
def main_process(goal_profit = 15):
    # 결과리스트
    resultList = []

    # 전체 종옥목록
    last_digit = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # stockList = Stc001.objects.filter(face_price__gt=0, tot_value__lte=70000000000)
    # stockList = Stc001.objects.filter(face_price__gt=0)
    stockList = Stc001.objects.filter(face_price__gt=0, stc_id='086900')
    # stockList = Stc001.objects.filter(face_price__gt=0, id__lt=10)

    # 전체 종목 대상
    for stock in stockList:

        try:
            # roe 10년, bps data추출
            crawling_data = crawler.find_one_stock_values(stock.stc_id)
            roes = crawling_data["roe"]
            dvsn = crawling_data["dvsn"]
            memo = crawling_data["memo"]
            diss = crawling_data["dis"]
            bps = crawling_data["bps"]
            price = crawling_data["price"]

            # 10년 roe 바탕으로 예측 roe 산출
            avg_roe_stDev = calculator_avg_roe(roes)
            avg_roe = avg_roe_stDev["avg_roe"]
            st_dev = avg_roe_stDev["standard_deviation"]

            # 10년 후 예상되는 순자산 가치 산출
            if avg_roe == 0:
                estimate_value = 0
            else:
                estimate_value = float(bps) * pow((1 + (avg_roe / 100)), 10)

            # 연간 수익률 추정
            if estimate_value == 0:
                annul_earning = 0
            else:
                annul_earning = pow((estimate_value / float(price)), 0.1)

            # 배당률 평균 계산
            avg_dis = calculator_avg_dis(diss)


            # 목표매수가
            goal_price = estimate_value / (pow(1+(float(goal_profit)/100), 10))

            # 판단
            if annul_earning == 0:
                judge_context = ""
            elif (annul_earning - 1) * 100 >= float(goal_profit):
                judge_context = "현재가 매수고려"
            elif (annul_earning - 1) * 100 < float(goal_profit):
                judge_context = str(round(goal_price))+" 이상인경우 매수고려"
            else:
                judge_context = ""

            resultList.append({"stc_id": stock.stc_id,
                               "stc_name": stock.stc_name,
                               "stc_dvsn": dvsn,
                               "stc_memo": memo,
                               "price": price,
                               "avg_roe": round(avg_roe, 2),
                               "st_dev": round(st_dev, 2),
                               "estimate_value": round(estimate_value, 2),
                               "annul_earning": round((annul_earning - 1) * 100, 2),
                               "avg_dis": round(avg_dis, 2),
                               "judge_context": judge_context})

        except Exception as e:
            print(stock.stc_id)
            print(e)

    return resultList
