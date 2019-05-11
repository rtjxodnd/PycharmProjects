from django.shortcuts import render
from invest.forms import *
import logging


def list(request):
    stockList = Stc001.objects.all()
    logging.debug('Debug Message')
    logging.error('error Message')
    return render(request, 'invest/list.html', {'stockList': stockList})
