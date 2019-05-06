"""
    File: KeyChord.py

    Author: Eli Yale
"""

from numpy.random import choice
import music21
import inspect
import string
import random

class KeyChord():
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
                #make this a pramter of the time signature
                c.duration.quarterLength = 4.0
                chord_type = music21.harmony.chordSymbolFigureFromChord(c, True)[1]
                new_part.append(c)

            

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


    def get_one_possible_harmonized_chords(self, keyName):
        curKey = music21.key.convertKeyStringToMusic21KeyString(keyName)
        if curKey.isupper():
            curScale = music21.scale.MajorScale(curKey)

        else:
            curScale = music21.scale.MinorScale(curKey)

        
        scalePitches = []
        for p in curScale.getPitches(curKey + "5", curKey + "6"):
            scalePitches.append(p)

        # finds harmonizing chord and prints i       
        i = random.randint(0,7)
        pitch1 = scalePitches[i]
        pitch2 = scalePitches[(i + 2) % 7]
        pitch3 = scalePitches[(i + 4) % 7]
        finalChord = music21.chord.Chord([pitch1, pitch2, pitch3])
        return music21.harmony.chordSymbolFigureFromChord(finalChord)

    def get_all_possible_harmonized_chords(self, keyName):
        curKey = music21.key.convertKeyStringToMusic21KeyString(keyName)
        if curKey.isupper():
            curScale = music21.scale.MajorScale(curKey)

        else:
            curScale = music21.scale.MinorScale(curKey)

        
        scalePitches = []
        for p in curScale.getPitches(curKey + "5", curKey + "6"):
            scalePitches.append(p)


        possibleHarmonizedChords = []
        # finds harmonizing chord and prints i

        for i in range(0, 7):
            pitch1 = scalePitches[i]
            pitch2 = scalePitches[(i + 2) % 7]
            pitch3 = scalePitches[(i + 4) % 7]

            finalChord = music21.chord.Chord([pitch1, pitch2, pitch3])
            possibleHarmonizedChords.append(music21.harmony.chordSymbolFigureFromChord(finalChord, False))

        return possibleHarmonizedChords