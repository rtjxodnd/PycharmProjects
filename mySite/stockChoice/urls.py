from django.urls import path
from stockChoice.views import *

app_name = 'stockChoice'
urlpatterns = [
    path('', index, name='index'),
    path('magic-formula/', get_magic_formula, name='getMagicFormula'),
]
