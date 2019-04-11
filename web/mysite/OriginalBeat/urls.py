from django.urls import path
from . import views

app_name = 'OriginalBeat'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('project/', views.project, name = 'project')
    #path('<int:name_id>/', views.detail, name='detail'),
]