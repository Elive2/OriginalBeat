"""
    File: Markov.py

    Description: This class contains the implmentation of the Markov class
    This is a model that can be used in the beat engine.

    Author: Eli Yale

    Date Created: January 31, 2019

    TODO:

    [ ] - context injection, maybe take jump aound with the state
    a bit, instead of doing a random walk

"""

import os
from pathlib import Path
from MarkovifyCustom import Chain

from utils import *

midifiles_directory = Path("../data/midifiles/")

class MarkovKey():
    """
    class: Markov()

    Description: This is a model class that can generate music. It is a standard markov
    chain using a corpus of midifiles. It provides methods to build the chain and generate
    with it. It takes a Beat object as its input data

    Things to try
    1. notes chords rest
    2. differnt states
    """

    def __init__(self, beat_instance):
        """
            function: __init__

            description: initalize a Markov model

            Parameters:
                beat_instance: (Beat) an instance of the beat class
                    Required Attributes:
                        The beat_instance must have:
        """

        self._beat = beat_instance

        self._state_size = 3
        print("building corpus")
        self._build_corpus_basic()
        self._build_input_chain()
        self._build_model_chain()

    def _build_input_chain(self):
        self._input_corpus = [[]]

        self._input_corpus[0] = get_notes_chords_rests(self._beat._midi_upload_file_path)
        self._input_chain = Chain(self._input_corpus, self._state_size)
        output = self._input_chain.walk()

    def _build_corpus_basic(self):
        """
            Function: _build_corpus_basic

            description: build a basic corpus where each run is the raw
            song data returned from notes chords rests. the corpus is
            built in place and saved in self._corpus
        """

        self._corpus = []
        for filename in os.listdir(str(midifiles_directory)):
            if filename.endswith(".mid"): 
                path = midifiles_directory / filename
                song_data = get_notes_chords_rests(path)
                self._corpus.append(song_data)
                continue
            else:
                continue

        print("corpus length:")
        print(len(self._corpus))


    def _build_model_chain(self):
        self._chainerator = Chain(self._corpus, self._state_size)
        self._output = self._chainerator.walk()
        print(self._output)
        