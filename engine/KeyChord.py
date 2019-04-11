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

        for el in midi.recurse():
            print(el)
        print("len parts", len(midi.parts))

        midi.parts[0].makeMeasures(inPlace=True)
        print(len(midi.getElementsByClass('Measure')))

        ms = midi.parts[0].measures(0,None)

        for element in ms:
            print(element)



