"""
    File: KeyChord.py

    Author: Eli Yale
"""

from numpy.random import choice
import music21

class KeyChord():
    """
        Class: KeyChord

        Description: A very crude generator
    """

    def __init__(self, beatInsatnce):
        self._beat = beatInsatnce


        print(self._beat._midi_upload_file_path)
        midi = music21.converter.parse(self._beat._midi_upload_file_path)

        midi.parts[0].makeMeasures(inPlace=True)
        ms = midi.parts[0].measures(0,None)

        for measure in ms:
            measureNotes = []
            for note in measure:
                if isinstance(note, music21.note.Note):
                    measureNotes.append(note.pitch.pitchClass)

            print(measureNotes)



