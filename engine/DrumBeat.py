"""
    File: DrumBeat.py

    Author: Matt Kordonsky
"""

from numpy.random import choice
import music21
import inspect
import string
import random

class DrumBeat():
    """
        Class: DrumBeat

        Description: Generates Bass Drums for every quarter note of the midi melody. Adds high hat based on the peak of the music
    """

    def __init__(self, beatInsatnce):
        self._beat = beatInsatnce
        

    def generate(self):

        #all possible percussive sounds for potential use
        #
        acoustic_bass_drum = 35
        bass_drum_1 = 36
        closed_high_hat = 42
        pedal_high_hat = 44
        open_high_hat = 46
        crash_cymbal_1 = 49
        crash_cymbal_2 = 57
        


        #begin operating on the combined stream
        self._beat.midi_stream.parts[0].makeMeasures(inPlace=True)
        ms = self._beat.midi_stream.parts[0].measures(0,None)

        bass_drum = music21.instrument.BassDrum()
        high_hat = music21.instrument.HiHatCymbal()

        new_part = music21.stream.Part()
        new_part.insert(0, bass_drum)
        #new_part.insert(0, high_hat)
        
        #print(bass_drum)
        for measure in ms:
            for note in measure:
                if isinstance(note, music21.note.Note):
                    n = music21.note.Note(35)
                    n.duration.quarterLength = 1.0
                    new_part.append(n)

        #mfp =       
        self._beat.midi_stream.append(new_part)

        self._beat.midi_stream_drums = music21.stream.Stream(new_part)
