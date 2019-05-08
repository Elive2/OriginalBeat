from django.urls import path
from . import views

app_name = 'OriginalBeat'
urlpatterns = [
    path('', views.index, name = 'index'),
    path('project/', views.project, name = 'project'),
    path('<int:name_id>/', views.detail, name='detail'),
    path('midi/', views.midi, name='midi'),
    path('midi/melody/', views.midi_melody, name='midi_melody'),
    path('midi/harmony/', views.midi_harmony, name='midi_harmony'),
    path('download/', views.download, name='download'),
    path('about/', views.about, name = 'about'),
    path('contact/', views.contact, name = 'contact')
]
