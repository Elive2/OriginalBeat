"""
    File: KeyChord.py

    Author: Matt Kordonsky
"""

from numpy.random import choice
import music21
import inspect
import string
import random

class KeyChord2():
    """
        Class: KeyChord

        Description: A very crude generator
    """

    def __init__(self, beatInsatnce):
        self._beat = beatInsatnce
        
        #midi.quantize([1], processOffsets=True, processDurations=True, inPlace=True)
        #self._chord_reducer(midi)

    def generate(self):
        #begin operating on the combined stream
        self._beat.midi_stream.parts[0].makeMeasures(inPlace=True)
        ms = self._beat.midi_stream.parts[0].measures(0,None)

        new_part = music21.stream.Part()
        
        for measure in ms:
            measureNotes = []
            for note in measure:
                if isinstance(note, music21.note.Note):
                    measureNotes.append(note.pitch.pitchClass)

            if (len(measureNotes) > 0):
                c = music21.chord.Chord(list(set(measureNotes)))

                bass_pitch = c.bass()
                octave = bass_pitch.octave
                
                key = music21.harmony.chordSymbolFigureFromChord(c, False)
                key = key[0] + key[1] 
                new_key = music21.key.Key(key)

                new_chord = self.get_one_possible_harmonized_chords(new_key, octave)
               
                #make this a pramter of the time signature
                new_chord.duration.quarterLength = 4.0
                chord_type = music21.harmony.chordSymbolFigureFromChord(new_chord, True)[1]
                
                new_part.append(new_chord)

            

        self._beat.midi_stream.append(new_part)

        self._beat.midi_stream_harmony = music21.stream.Stream(new_part)

        #key = music21.key.Key('a')
        #print(key.getChord(music21.pitch.Pitch(0), music21.pitch.Pitch(12)).pitches)


        #print("DONE")



    def _chord_reducer(self, midi):
            print("measure chord: ")
            cr = music21.analysis.reduceChords.ChordReducer()
            newS = cr.reduceMeasureToNChords(midi, 3, trimBelow=0.3)
            newS.show('text')

    def get_one_possible_harmonized_chords(self, key, octave):
        print(key.pitches)

        scalePitches = key.pitches

        # finds harmonizing chord and prints i       
        i = random.randint(0,7)
        pitch1 = scalePitches[i]
        pitch2 = scalePitches[(i + 2) % 7]
        pitch3 = scalePitches[(i + 4) % 7]
        finalChord = music21.chord.Chord([pitch1, pitch2, pitch3])
        print(finalChord)
        return finalChord