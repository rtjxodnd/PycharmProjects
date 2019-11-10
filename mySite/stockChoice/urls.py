from django.urls import path
from stockChoice.views import *

app_name = 'stockChoice'
urlpatterns = [
    path('', index, name='index'),
    path('magic-formula/', get_magic_formula, name='getMagicFormula'),
    path('get-bond-style-stock/', get_bond_style_stock, name='getBondStyleStock'),
    path('get-material-stock/', get_material_stock, name='getMaterialStock'),
    path('result-bond-style-stock/', result_bond_style_stock, name='resultBondStyleStock'),
    path('result-material-stock/', result_material_stock, name='resultMaterialStock'),
]
