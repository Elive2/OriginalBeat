from django.urls import path
from . import views

app_name = 'OriginalBeat'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('<int:name_id>/', views.detail, name='detail'),
]