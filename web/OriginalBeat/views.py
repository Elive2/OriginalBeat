"""
    File: views.py

    Description:

    TODO:

    [ ] - projects
    [ ] - figure out why uploads are being saved with the file name, not just the username
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
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from music21 import stream, note, midi, duration



# TODO: This Shouldn't be hard coded
if(os.environ['PROJ_DIR']):
    sys.path.append(os.environ['PROJ_DIR'])
else:
    print("PLEASE SET THE ENVIRONMENT VARIABLE 'PROJ_DIR' to the root of OriginalBeat")
USR_FILE_PATH = os.path.join(os.path.join(settings.BASE_DIR , 'OriginalBeat'),'userfiles')
from engine import BeatEngine

@ensure_csrf_cookie
@require_http_methods(["GET"])
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

@require_http_methods(["GET"])
def about(request):
    return render(request, 'OriginalBeat/about.html')

@require_http_methods(["GET"])
def contact(request):
    return render(request, 'OriginalBeat/contact.html')

@require_http_methods(["GET"])
def project(request):
    if request.user.is_authenticated:
        return render(request, 'OriginalBeat/project.html')
    else:
        return HttpResponseRedirect('/accounts/login/')

def detail(request, song_id):
    song = get_object_or_404(songName, pk = song_id)
    return render(request, 'OriginalBeat/index.html', {'song':song})

@require_http_methods(["GET", "POST"])
def midi_upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST' and request.FILES['Midi']:
            print("in post request")
            myfile = request.FILES['Midi']
            print("got file")
            fs = FileSystemStorage()
            print("created fs")
            #handle projects here, for now just delete the file if it exists
            if(fs.exists(request.user.username + '_' + myfile.name)):
                fs.delete(request.user.username + '_' + myfile.name)
                print("deleted file")

            filename = fs.save(request.user.username + '_' + myfile.name, myfile)
            print("saved file")
            uploaded_file_url = fs.url(filename)
            midi_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '.mid')
            midi_melody_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_melody.mid')
            midi_harmony_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_harmony.mid')
            midi_drums_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_drums.mid')
            engine = BeatEngine.BeatEngine(fs.location + '/' + uploaded_file_url, midi_output_location, midi_melody_output_location, midi_harmony_output_location, midi_drums_output_location, None)
            print("created engine")

            return render(request, 'OriginalBeat/project.html')
        else:
            output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '.mid')
            return FileResponse(open(output_location, 'rb'))
    else:
        return HttpResponseRedirect('/accounts/login/')

def download(request):
    midi_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '.mid')
    #return serve(request, midi_output_location)
    return FileResponse(open(midi_output_location, 'rb'))

@require_http_methods(["GET"])
def midi_melody(request):
    if request.user.is_authenticated:
        output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_melody.mid')
        return FileResponse(open(output_location, 'rb'))
    else:
        return HttpResponseRedirect('/accounts/login/')

@require_http_methods(["GET"])
def midi_harmony(request):
    if request.user.is_authenticated:
        output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_harmony.mid')
        return FileResponse(open(output_location, 'rb'))
    else:
        return HttpResponseRedirect('/accounts/login/')

@csrf_exempt
@require_http_methods(["POST"])
def input_midi(request):
    midi_json = json.loads(request.body)

    midi_stream = stream.Stream()
    for input_note in midi_json:
        new_note = note.Note(input_note['midiNumber'])
        new_note.offset = input_note['time'] * 5
        new_note.duration = duration.Duration(input_note['duration'] * 5)
        midi_stream.append(new_note)

    uploaded_file_path = os.path.join(os.path.join(USR_FILE_PATH,'uploads'), request.user.username + '.mid')
    mf = midi.translate.streamToMidiFile(midi_stream)
    mf.open(uploaded_file_path, 'wb')
    mf.write()
    mf.close()
    print("saved input to disk")

    midi_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '.mid')
    midi_melody_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_melody.mid')
    midi_harmony_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_harmony.mid')
    midi_drums_output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_drums.mid')
    engine = BeatEngine.BeatEngine(uploaded_file_path, midi_output_location, midi_melody_output_location, midi_harmony_output_location, midi_drums_output_location, None)
    print("created engine")

    return render(request, 'OriginalBeat/project.html')

@require_http_methods(["GET"])
def midi_drums(request):
    if request.user.is_authenticated:
        output_location = os.path.join(os.path.join(USR_FILE_PATH,'outputs'), request.user.username + '_drums.mid')
        return FileResponse(open(output_location, 'rb'))
    else:
        return HttpResponseRedirect('/accounts/login/')

