from invest.models import Stc001
from stockChoice.crawler import get_bond_style_stock as crawler


###########################################################
# Main 처리: data 읽어서 주식기본 테이블에 저장한다.
###########################################################
def main_process(stock_list):
    return stock_list