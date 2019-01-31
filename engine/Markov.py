"""
    File: Markov.py

    Description: This class contains the implmentation of the Markov class
    This is a model that can be used in the beat engine.

    Author: Eli Yale

    Date Created: January 31, 2019

"""

import os
from pathlib import Path

from utils import *

midifiles_directory = Path("../data/midifiles/")

class Markov():
    """
    class: Markov()

    Description: This is a model class that can generate music. It is a standard markov
    chain using a corpus of midifiles. It provides methods to build the chain and generate
    with it. It takes a Beat object as its input data
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

        print("building chain")
        #self._build_chain()

        #not sure what needs to be done on initalization yet
        #gotta build the chain first

    def _build_corpus(self):
        for filename in os.listdir(str(midifiles_directory)):
            if filename.endswith(".mid"): 
                print(midifiles_directory / filename)

                continue
            else:
                continue


    def _build_chain(self):
        
        pass
        #build the chain heregi
        