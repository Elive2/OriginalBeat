"""
    File: Markov.py

    Description: This class contains the implmentation of the Markov class
    This is a model that can be used in the beat engine.

    Author: Eli Yale

    Date Created: January 31, 2019

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

        print("building corpus")
        self._build_corpus()
        self._build_chain()
        notes_chords_rests_to_midi(self._output)

        #not sure what needs to be done on initalization yet
        #gotta build the chain first

    def _build_corpus(self):
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


    def _build_chain(self):
        self._chainerator = Chain(self._corpus, 2)
        self._output = self._chainerator.walk()
        print(self._output)
        #build the chain heregi
        