from django.shortcuts import render
from stockChoice.crawler.get_magic_formula import main_process as getMagicFormula
from stockChoice.main.bond_style_stock import main_process as bondStyleStock
from stockChoice.main.material_stock import main_process as materialStock

def index(request):
    return render(request, 'stock-choice/index.html')


def get_magic_formula(request):
    stockList = getMagicFormula()
    return render(request, 'stock-choice/magic-formula.html', {'stockList': stockList})


def get_bond_style_stock(request):
    return render(request, 'stock-choice/get-bond-style-stock.html')


def get_material_stock(request):
    return render(request, 'stock-choice/get-material-stock.html')


def result_bond_style_stock(request):
    stockList = bondStyleStock(request.POST.get("profit"))
    return render(request, 'stock-choice/result-bond-style-stock.html', {'stockList': stockList})


def result_material_stock(request):
    stockList = materialStock(request.POST.get("profit"))
    return render(request, 'stock-choice/result-material-stock.html', {'stockList': stockList})