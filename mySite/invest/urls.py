from django.urls import path
from invest.views import *

app_name = 'invest'
urlpatterns = [
    path('', index, name='index'),
    path('list/', list, name='list'),
    path('get-base-info/', get_base_info, name='getBaseInfo'),
    path('get-daily-info/', get_daily_info, name='getDailyInfo'),
    path('insert-base-info/', insert_base_info, name='insertBaseInfo'),
    path('insert-daily-info/', insert_daily_info, name='insertDailyInfo'),
]
