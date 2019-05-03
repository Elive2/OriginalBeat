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

    TODO: 

    [ ] - figure out why it says "failed on path"

"""
import mido
#from MarkovKey import MarkovKey
#from BayesNet import BayesNet
import sys, os

#TODO: this shouldn't be hardcoded
sys.path.append(os.environ['PROJ_DIR'] + '/engine')
from KeyChord import KeyChord
import music21
import os
from Beat import Beat #for the beat class
from utils import *



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
    def __init__(self, midi_upload_file_path, midi_file_output_path, model_type):
        """
            function: __init__

            description: initalize a beat engine and insantiate a beat project

            Parameters:
                midi_upload_file_path -- (string) absolute file path to a mid file
                model_type -- (string) name of model ie 'markov'
        """

        self._beat = Beat(midi_upload_file_path, midi_file_output_path)

        #NOTE: Will eventually set this to a countBeats() method for variable
        #length midis, for now it is hardocded as 8
        #self._beat.bars = 8å

        #NOTE: this will eventually be a call to findTempo(), but for now
        #it is hardocded to 120 bpm
        self._beat.tempo = 120

        self._beat.key = findKey(midi_upload_file_path)
        #print(self._beat.key)

        self._beat.notes_chords_rests = get_notes_chords_rests(midi_upload_file_path)

        #read and parse the midifile
        self._beat.midi_stream = music21.converter.parse(self._beat._midi_upload_file_path)

        model = KeyChord(self._beat)
        #generate the output in place on self._beat
        model.generate()
        # test for harmonized chords
        print()
        print("Random Chord Choice: " + model.get_one_possible_harmonized_chords("C#"))
        print()
        test = model.get_all_possible_harmonized_chords("C#")
        for i in test:
            print(i)


        #write the output
        mf = music21.midi.translate.streamToMidiFile(self._beat.midi_stream)
        mf.open(midi_file_output_path, 'wb')
        mf.write()
        mf.close()


    #saving this for later
    def _parse_midi_file(filename):
        midi_list = []
        mid = mido.MidiFile(filename)
        for msg in mid.play():
            print(msg.note);


def main():
    engine = BeatEngine('../data/midifiles/Aminor.mid', '../data/output/output.mid', None)


if __name__ == '__main__':
    main()

