from bs4 import BeautifulSoup
import requests


# 한건의 data 추출
def find_one_stock_values(stc_id):
    # 데이터 탐색
    url = "http://search.itooza.com/search.htm?seName="+str(stc_id)
    page_call_result = requests.get(url)
    bs_obj = BeautifulSoup(page_call_result.content.decode('euc-kr', 'replace'), "html.parser")

    # 종목기본정보
    stc_div = bs_obj.find("div", {"class": "item-head"})
    stc_dvsn = stc_div.find("span", {"class": "code category"}).text
    stc_memo = stc_div.find("p", {"class": "desc"}).text

    # roe, 배당률
    row_div = bs_obj.find("div", {"id": "indexTable2"})
    row_table = row_div.find("table", {"border": "1", "class": "ex"})
    row_tbody = row_table.find("tbody")
    row_trs = row_tbody.find_all("tr")
    roe_tr = row_trs[7]
    dis_tr = row_trs[6]
    roe_tds = roe_tr.find_all("td")
    dis_tds = dis_tr.find_all("td")

    # bps
    bps_div = bs_obj.find("div", {"id": "stockItem"}).find("div", {"class": "item-data1"})
    bps_trs = bps_div.find_all("tr")
    bps_tr = bps_trs[1]
    bps_tds = bps_tr.find_all("td")
    bps = bps_tds[4].text.replace(",", "")

    # price
    bps_div = bs_obj.find("div", {"id": "stockItem"}).find("div", {"class": "item-detail"})
    price = bps_div.find("span").text.replace(",", "")

    # 필요 데이터 추출
    result_value = {"dvsn": stc_dvsn,
                    "memo": stc_memo,
                    "roe":
                        {"roe0": roe_tds[0].text, "roe1": roe_tds[1].text, "roe2": roe_tds[2].text, "roe3": roe_tds[3].text,
                         "roe4": roe_tds[4].text, "roe5": roe_tds[5].text, "roe6": roe_tds[6].text, "roe7": roe_tds[7].text,
                         "roe8": roe_tds[8].text, "roe9": roe_tds[9].text, "roe10": roe_tds[10].text, "roe11": roe_tds[11].text},
                    "dis":
                        {"dis0": dis_tds[0].text, "dis1": dis_tds[1].text, "dis2": dis_tds[2].text, "dis3": dis_tds[3].text,
                         "dis4": dis_tds[4].text, "dis5": dis_tds[5].text, "dis6": dis_tds[6].text, "dis7": dis_tds[7].text,
                         "dis8": dis_tds[8].text, "dis9": dis_tds[9].text, "dis10": dis_tds[10].text, "dis11": dis_tds[11].text},
                    "bps": bps,
                    "price": price}


    return result_value
