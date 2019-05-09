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

        Description: Generates Bass Drum for every quarter note of the midi melody. Adds high hat based on the peak of the music
    """

    def __init__(self, beatInsatnce):
        self._beat = beatInsatnce
        

    def generate(self):

        #all possible percussive sounds for potential use
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
        

        new_bass_part = music21.stream.Part()
        new_bass_part.insert(0, bass_drum)
        
        new_hh_part = music21.stream.Part()
        new_hh_part.insert(0, high_hat)
        
        for measure in ms:
            for note in measure:
                
                if isinstance(note, music21.note.Note):
                    if random.randint(1, 101) > 20:
                        bass = music21.note.Note(acoustic_bass_drum)
                        bass.duration.quarterLength = 1.0
                        new_bass_part.append(bass)   
                    else:
                        bass = music21.note.Rest()
                        bass.duration.quarterLength = 1.0
                        new_bass_part.append(bass)     
                    
        for measure in ms:
            for note in measure:
                if isinstance(note, music21.note.Note):
                    
                    hh1 = music21.note.Note(closed_high_hat)
                    hh1.duration.quarterLength = 0.5
                    new_hh_part.append(hh1)

                    rnd = random.randint(1, 101)
                    if rnd > 50:
                        hh_and = music21.note.Note(closed_high_hat)
                        hh_and.duration.quarterLength = 0.5
                        new_hh_part.append(hh_and)
                    else:
                        hh_and = music21.note.Rest()
                        hh_and.duration.quarterLength = 0.5
                        new_hh_part.append(hh_and)
        
        self._beat.midi_stream.append(new_bass_part)
        
        self._beat.midi_stream.append(new_hh_part)
        

        self._beat.midi_stream_drums = music21.stream.Stream()
        
        self._beat.midi_stream_drums.append(new_bass_part)
        self._beat.midi_stream_drums.append(new_hh_part)
        
        