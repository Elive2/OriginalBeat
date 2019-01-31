"""
	File: BeatEngine.py

	Description: This file is the main genereation engine and thus is the name
	of the entire module that does the generation. This script runs server side
	and is invoked by the django process whenever a midiupload is ready to be
	proccessed.

    TODO: Figure out if we should instantiate one beat engine, and process
    all requests with it, or instantiate one beat engine per each request.

    I think for now I will go with one beat engine per request.
    This allows me to not have to woory about queing requests, and many can
    be processed at once with seperate beatengines. The problem
    that may arises is space complexity if too many people send
    in a file at once. But another benefit is we could easily extend
    this class to javascript and run the engine client side.

	Author: Eli Yale
	Date Created: January 23, 2018

    NOTE: keys are represented with music 21 notation
            B = B major
            b = B minor
            B- = B flat major
            b- = B flat minor

"""

import mido
from Crude import Crude
import music21
import os
from Beat import Beat #for the beat class



class BeatEngine():
    """
    class: BeatEngine()
    
    Description: The main class to which a raw uploaded midi file is fed.
    It does pre processing on the midifile and prepares it for
    a generator model. Then it instantiates a generator model 
    and feeds the input. The input to a model is a instance of the
    beat class, see beat.py for more info. So this class, prepares
    the beat object for the model.

    Public Functions: 
        self._play : Play the file in progress for testing purposes
        self._piano_roll: get a piano roll

    Private instance variables:

        self._beat : an instance of the beat class that will be built
                     by the engine

    TODO:
        pianoroll
        playsong

    """
    def __init__(self, midi_upload_file_path, model_type):
        """
            function: __init__

            description: initalize a beat engine and insantiate a beat project

            Parameters:
                midi_upload_file_path -- (string) absolute file path to a mid file
                model_type -- (string) name of model ie 'markov'
        """

        self._beat = Beat(midi_upload_file_path)

        #NOTE: Will eventually set this to a countBeats() method for variable
        #length midis, for now it is hardocded as 8
        #self._beat.bars = 8

        #NOTE: this will eventually be a call to findTempo(), but for now
        #it is hardocded to 120 bpm
        self._beat.tempo = 120

        self._beat.key = self._findKey(midi_upload_file_path)

        self._beat.notes_chords_rests = self._get_notes_chords_rests(midi_upload_file_path)
        


    def _findKey(self, filename):
        """
            function: _findKey

            Description: private member function to compute the key of 
            a given midifile

            Parameters: 
                filename -- (string) absolute file path to a midi
        """
            
        mid = mido.MidiFile(filename)

        #first check if there is a meta message with the key signature
        for msg in mid:
            if msg.type == 'key_signature':
                return msg.key

        mf = music21.midi.MidiFile()
        mf.open(filename)
        mf.read()
        s = music21.midi.translate.midiFileToStream(mf)

        #this seems to be fairly slow on large midifiles
        key = music21.analysis.discrete.analyzeStream(s, 'Krumhansl')

        #can get lots of cool stuff from the key, ie, relative major
        #scales, tonic and even transpose
        #uncomment below to see what

        #print(dir(key))

        return key.tonicPitchNameWithCase

    def _get_notes_chords_rests(self, path):
        """
            Function: _get_notes_chords_rests

            Description: Extract into a list all chords, notes, and rests in a midifile
            This looks at only keyboard type insturmnets.

            Parameters:
                path -- (string) absolute file path to a midifile

            NOTE: This expects chords to have their notes played at exactly the same time.
            Offset iterator returns a list of all events that occur at the same offset.
            Will need to do some sort of tolerance snapping cause user inputted melodies
            can't be expected to be right on beat.
        """

        keyboard_instrument = ["KeyboardInstrument", "Piano", "Harpsichord", "Clavichord", "Celesta"]
        try:
            midi = music21.converter.parse(path)
            parts = music21.instrument.partitionByInstrument(midi)
            #parts.show('text')
            note_list = []
            for music_instrument in range(len(parts)):
                if parts.parts[music_instrument].id in keyboard_instrument:
                    for element_by_offset in music21.stream.iterator.OffsetIterator(parts[music_instrument]):
                        for entry in element_by_offset:
                            if isinstance(entry, music21.note.Note):
                                note_list.append(str(entry.pitch))
                            elif isinstance(entry, music21.chord.Chord):
                                note_list.append('.'.join(str(n) for n in entry.normalOrder))
                            elif isinstance(entry, music21.note.Rest):
                                note_list.append('Rest')
            print(note_list)
            return note_list

        except Exception as e:
            print("failed on ", path, "with exception: ", e)
            pass


    #saving this for later
    def _parse_midi_file(filename):
        midi_list = []
        mid = mido.MidiFile(filename)
        for msg in mid.play():
            print(msg.note);


def main():
    engine = BeatEngine('../data/midifiles/HappyBirthday.mid', None)

if __name__ == '__main__':
    main()

