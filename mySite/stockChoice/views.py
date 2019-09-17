from django.shortcuts import render
from stockChoice.crawler.get_magic_formula import main_process as getMagicFormula
from stockChoice.main.bond_style_stock import main_process as bondStyleStock
from stockChoice.main.bond_style_stock_excel import main_process as bondStyleStockExcel

def index(request):
    return render(request, 'stock-choice/index.html')


def get_magic_formula(request):
    stockList = getMagicFormula()
    return render(request, 'stock-choice/magic-formula.html', {'stockList': stockList})

def get_bond_style_stock(request):
    stockList = bondStyleStock()
    return render(request, 'stock-choice/bond-style-stock.html', {'stockList': stockList})

def get_bond_style_stock_excel(request):
    stockList = bondStyleStockExcel(request.POST.get("stock_list"))
    return render(request, 'stock-choice/bond-style-stock-excel.html', {'stockList': stockList})
