from django.urls import path
from stockChoice.views import *

app_name = 'stockChoice'
urlpatterns = [
    path('', index, name='index'),
    path('magic-formula/', get_magic_formula, name='getMagicFormula'),
    path('bond-style-stock/', get_bond_style_stock, name='getBondStyleStock'),
    path('bond-style-stock-excel/', get_bond_style_stock_excel, name='getBondStyleStockExcel'),
]
