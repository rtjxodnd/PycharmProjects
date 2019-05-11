from django.urls import path
from community.views import *

app_name = 'community'
urlpatterns = [
    path('write/', write, name='write'),
    path('list/', list, name='list'),
    path('view/<num>', view),
]
