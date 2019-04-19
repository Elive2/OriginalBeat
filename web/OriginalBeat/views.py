from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db import models
from OriginalBeat.models import songName
from django.views.decorators.csrf import ensure_csrf_cookie
from django.core.files.storage import FileSystemStorage
from django.http import JsonResponse
from django.views.static import serve
from django.http import FileResponse
import os
import json

@ensure_csrf_cookie
def index(request):
    latestSongList = songName.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('OriginalBeat/index.html')
    context = { 'latestSongList': latestSongList}
    # output = ', '.join([s.name for s in latestSongList])
    #return HttpResponse(template.render(context, request))
    return render(request, 'OriginalBeat/index.html', context)

def project(request):
	return render(request, 'OriginalBeat/project.html')
	
def detail(request, song_id):
    song = get_object_or_404(songName, pk = song_id)
    return render(request, 'OriginalBeat/index.html', {'song':song})

def midi(request):
    if request.method == 'POST' and request.FILES['Midi']:
        myfile = request.FILES['Midi']
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        return render(request, 'OriginalBeat/project.html')
    else:
        midi_path = 'OriginalBeat/static/userfiles/Aminor.mid'
        return FileResponse(open(midi_path, 'rb'))

def download(request):
    midi_path = 'OriginalBeat/static/userfiles/Aminor.mid'
    return serve(request, os.path.basename(midi_path), os.path.dirname(midi_path))




