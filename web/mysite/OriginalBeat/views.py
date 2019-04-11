from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import render, get_object_or_404
from django.db import models
from OriginalBeat.models import songName


def index(request):
    latestSongList = songName.objects.order_by('-pub_date')[:5]
    #template = loader.get_template('OriginalBeat/index.html')
    context = { 'latestSongList': latestSongList}
    # output = ', '.join([s.name for s in latestSongList])
    #return HttpResponse(template.render(context, request))
    return render(request, 'OriginalBeat/index.html', context)

def project(request):
	return render(request, 'OriginalBeat/project.html')
# def detail(request, song_id):
#     song = get_object_or_404(songName, pk = song_id)
#     return render(request, 'OriginalBeat/index.html', {'song':song})

