"""
    File: KeyChord.py

    Author: Eli Yale
"""

from numpy.random import choice
import music21
import inspect

class KeyChord():
    """
        Class: KeyChord

        Description: A very crude generator
    """

    def __init__(self, beatInsatnce):
        self._beat = beatInsatnce


        print(self._beat._midi_upload_file_path)
        midi = music21.converter.parse(self._beat._midi_upload_file_path)
        #midi.quantize([1], processOffsets=True, processDurations=True, inPlace=True)
        self._manual_chords(midi)
        #self._chord_reducer(midi)


    def _manual_chords(self, midi):
        midi.parts[0].makeMeasures(inPlace=True)
        ms = midi.parts[0].measures(0,None)

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

            

        midi.append(new_part)

        mf = music21.midi.translate.streamToMidiFile(midi)
        mf.open('/Users/eliyale/Developer/scu/SeniorDesign/OriginalBeat/web/OriginalBeat/static/userfiles/output.mid', 'wb')
        mf.write()
        mf.close()

        key = music21.key.Key('a')
        #print(key.getChord(music21.pitch.Pitch(0), music21.pitch.Pitch(12)).pitches)


        #print("DONE")



    def _chord_reducer(self, midi):
            print("measure chord: ")
            cr = music21.analysis.reduceChords.ChordReducer()
            newS = cr.reduceMeasureToNChords(midi, 3, trimBelow=0.3)
            newS.show('text')


