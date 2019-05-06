"""
    File: KeyChord.py

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
        
        #midi.quantize([1], processOffsets=True, processDurations=True, inPlace=True)
        #self._chord_reducer(midi)

    def generate(self):
        acoustic_bass_drum = 35
        bass_drum_1 = 36
        closed_high_hat = 42 
        pedal_high_hat = 44
        open_high_hat = 46
        crash_cymbal_1 = 49
        crash_cymbal_2 = 57
        
        pm = music21.midi.percussion.PercussionMapper()

        """
        #begin operating on the combined stream
        self._beat.midi_stream.parts[0].makeMeasures(inPlace=True)
        ms = self._beat.midi_stream.parts[0].measures(0,None)

        new_part = music21.stream.Part()
        key_harm = KeyHarm(self._beat)
        input()

        key_harm.get_possible_harmonized_chords('C')


        for measure in ms:
            measureNotes = []
            for note in measure:
                if isinstance(note, music21.note.Note):
                    measureNotes.append(note.pitch.pitchClass)

            if (len(measureNotes) > 0):
                c = music21.chord.Chord(list(set(measureNotes)))
                #make this a pramter of the time signature
                c.duration.quarterLength = 4.0
                chord_type = music21.harmony.chordSymbolFigureFromChord(c, True)[1]
                new_part.append(c)

            

        self._beat.midi_stream.append(new_part)

        self._beat.midi_stream_harmony = music21.stream.Stream(new_part)

        #key = music21.key.Key('a')
        #print(key.getChord(music21.pitch.Pitch(0), music21.pitch.Pitch(12)).pitches)


        #print("DONE")
        """