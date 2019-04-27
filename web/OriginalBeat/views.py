"""
    File: views.py

    Description:

    TODO:

    [ ] - projects
"""

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
import os, sys
import json
from django.conf import settings
from django.shortcuts import HttpResponseRedirect
import os


# TODO: This Shouldn't be hard coded
if(os.environ['PROJ_DIR']):
    sys.path.append(os.environ['PROJ_DIR'])
else:
    print("PLEASE SET THE ENVIRONMENT VARIABLE 'PROJ_DIR' to the root of OriginalBeat")
USR_FILE_PATH = os.path.join(os.path.join(settings.BASE_DIR , 'OriginalBeat'),'userfiles')
from engine import BeatEngine

@ensure_csrf_cookie
def index(request):
    if request.user.is_authenticated:
        latestSongList = songName.objects.order_by('-pub_date')[:5]
        #template = loader.get_template('OriginalBeat/index.html')
        context = { 'latestSongList': latestSongList}
        # output = ', '.join([s.name for s in latestSongList])
        #return HttpResponse(template.render(context, request))
        return render(request, 'OriginalBeat/upload.html', context)
    else:
        return render(request, 'OriginalBeat/index.html')

def project(request):
    if request.user.is_authenticated:
        return render(request, 'OriginalBeat/project.html')
    else:
        return HttpResponseRedirect('/accounts/login/')
	
def detail(request, song_id):
    song = get_object_or_404(songName, pk = song_id)
    return render(request, 'OriginalBeat/index.html', {'song':song})

def midi(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['Midi']:
            myfile = request.FILES['Midi']
            fs = FileSystemStorage()
            #handle projects here, for now just delete the file if it exists
            if(fs.exists(request.user.username + '_' + myfile.name)):
                fs.delete(request.user.username + '_' + myfile.name)

            filename = fs.save(request.user.username + '_' + myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '.mid')
            engine = BeatEngine.BeatEngine(fs.location + '/' + uploaded_file_url, output_location, None)

            return render(request, 'OriginalBeat/project.html')
        else:
            output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '.mid')
            return FileResponse(open(output_location, 'rb'))
    else:
        return HttpResponseRedirect('/accounts/login/')

def download(request):
    midi_path = 'OriginalBeat/static/userfiles/output.mid'
    return serve(request, os.path.basename(midi_path), os.path.dirname(midi_path))




