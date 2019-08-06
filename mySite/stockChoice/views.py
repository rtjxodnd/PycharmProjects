from django.shortcuts import render
from stockChoice.crawler.get_magic_formula import main_process as getMagicFormula


def index(request):
    return render(request, 'stock-choice/index.html')


def get_magic_formula(request):
    stockList = getMagicFormula()
    return render(request, 'stock-choice/magic-formula.html', {'stockList': stockList})

