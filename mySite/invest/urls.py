from django.urls import path
from invest.views import *

app_name = 'invest'
urlpatterns = [
    path('', index, name='index'),
    path('list/', list, name='list'),
    path('get-base-info/', insert_base_info, name='insertBaseInfo'),
]
