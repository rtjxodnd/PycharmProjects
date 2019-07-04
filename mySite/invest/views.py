from django.shortcuts import render
from invest.forms import *
from invest.bizLogic.get_basic_stock_info import main_process as getBasicInfo
from invest.bizLogic.get_daily_stock_info import main_process as getDailyInfo


def index(request):
    return render(request, 'invest/index.html')


def list(request):
    stockList = Stc001.objects.all()
    return render(request, 'invest/list.html', {'stockList': stockList})


def get_base_info(request):
    return render(request, 'invest/get_base_info.html')


def insert_base_info(request):
    insert_quantity = getBasicInfo(request.POST.get("kospi_yn"), request.POST.get("kosdaq_yn"))
    return render(request, 'invest/result_base_info.html', {'insert_quantity': insert_quantity})


def get_daily_info(request):
    return render(request, 'invest/get_daily_info.html')


def insert_daily_info(request):
    insert_quantity = getDailyInfo(request.POST.get("input_dt").replace('-', ''))
    return render(request, 'invest/result_daily_info.html', {'insert_quantity': insert_quantity})


def delete_base_info(request, stc_id, stc_name, stc_dvsn, now_price, face_price, tot_value, pgm_id):
    Stc001(stc_id=stc_id, stc_name=stc_name, stc_dvsn=stc_dvsn, now_price=now_price, face_price=face_price, tot_value=tot_value, pgm_id=pgm_id ).save()
    return render(request, 'invest/result_base_info.html')

