from django.shortcuts import render
from invest.forms import *
from invest.bizLogic.get_basic_stock_info import main_process as getBasicInfo
from invest.bizLogic.get_daily_stock_info import main_process as getDailyInfo


def index(request):
    return render(request, 'invest/index.html')


def list(request):
    stockList = Stc001.objects.all()
    return render(request, 'invest/list.html', {'stockList': stockList})


def insert_base_info(request):
    insert_quantity = getBasicInfo('N', 'N')
    return render(request, 'invest/result_base_info.html', {'insert_quantity': insert_quantity})


def insert_daily_info(request):
    insert_quantity = getDailyInfo('20190625')
    return render(request, 'invest/result_daily_info.html', {'insert_quantity': insert_quantity})


def delete_base_info(request, stc_id, stc_name, stc_dvsn, now_price, face_price, tot_value, pgm_id):
    Stc001(stc_id=stc_id, stc_name=stc_name, stc_dvsn=stc_dvsn, now_price=now_price, face_price=face_price, tot_value=tot_value, pgm_id=pgm_id ).save()
    return render(request, 'invest/result_base_info.html')

