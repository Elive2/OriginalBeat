#was trying to fit my part in KeyChord


from numpy.random import choice
import music21
import inspect
import random

class KeyHarm():

    def __init__(self, beatInsatnce):
        self._beat = beatInsatnce
        print(self._beat._midi_upload_file_path)
        midi = music21.converter.parse(self._beat._midi_upload_file_path)
        self._manual_chords(midi)

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
        mf.open('../data/output/output1.mid', 'wb')
        mf.write()
        mf.close()

        key = music21.key.Key('a')
        print(key.getChord(music21.pitch.Pitch(0), music21.pitch.Pitch(12)).pitches)


        print("DONE")

    def get_possible_harmonized_chords(self, keyName):
        curKey = music21.key.convertKeyStringToMusic21KeyString(keyName)
        print(curKey)
        curKeyScale = music21.scale.ConcreteScale(tonic = curKey)
        print(curKeyScale)
        possibleHarmonizedChords = [curKeyScale.getTonic()]
        print(possibleHarmonizedChords)
        # creates a list of all pitches in the scale 
        for i in range(1, 7):
            newPitch = curKeyScale.next()
            print(newPitch)
            possibleHarmonizedChords.append(newPitch)
        print("fin")
        # finds harmonizing chord and prints i
        for iter in range(1, 8):
            pitch1 = possibleHarmonizedChords[iter]
            pitch2 = possibleHarmonizedChords[(iter + 2) % 8]
            pitch3 = possibleHarmonizedChords[(iter + 4) % 8]
            print(pitch1)
            print(pitch2)
            print(pitch3)
            finalChord = music21.chord.Chord([pitch1, pitch2, pitch3])
            print(music21.harmony.chordSymbolFigureFromChord(finalChord, True))
        
        print("DONE")


    def _chord_reducer(self, midi):
            print("measure chord: ")
            cr = music21.analysis.reduceChords.ChordReducer()
            newS = cr.reduceMeasureToNChords(midi, 3, trimBelow=0.3)
            newS.show('text')


