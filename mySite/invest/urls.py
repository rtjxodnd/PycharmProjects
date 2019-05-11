from django.urls import path
from invest import views

app_name = 'invest'
urlpatterns = [
    path('list/', views.list, name='list'),
]
