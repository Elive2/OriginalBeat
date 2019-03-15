"""
    File: BayesNet.py

    Description: This file defines a generator class based on a Bayesian Network

    [ ] - flag to specify to rebuild the chord chain
    [ ] - there has to be a more efficient way to build these probabilites
            with a one pass algorithm. I.E for each event scanned, determine which
            table it applies too, then add it to that tables running cond list and 
            increase the count of that event.
    [ ] - functions to fill in missing probabilities
    [ ] - rework schema - see notes

    Problem: the chords from in the m1_model come from the get_simul_chords_and_notes
    method which extracs chords from the second "part" of the midi file while the chords
    model uses get chords which extracts chords with the chordify method. This leads to
    two different chord sets found in the song data, and thus key errors in the probability
    tables, I need one unified method to find the chords, melody and voicing, data from the
    songs, then build the appropriate models from this, and then compute prob tables from
    the models.

    Solution 1: Simply one get_song_data method which extracts chords, notes and voicings
    into one uniform data structure
    Problem: There isn't enough chords in our dataset to get meaningful results. This is why
    using chordify was helpful, it gave me way more chords. maybe I can chodify into one track
    and sync it with the melody, this would be nice.

    Imporvements:

    1. Would be nice to automate the process of adding a node/parameter to the newtwork. Right now
    If you wanted to say add a base note, you would need to:
        1. add a self._cond_table_b0
        2. add the model to _load_from_disk
        3. add to build_alpha_model
        4. add function to build_cond_table_b0
        5. change get_song_data to have a base note parameter

    would be awesome to abstract this all away and just specify the network structure and have 
    the functions automatically gather the necessary song_data, then automatically generate the models
    and probability tables. But this would be A LOT of work

    2. Should Maybe have made seperate classes for each chord_model, note_model, note_chord_model
        ahh this is a good idea, then maybe if you want to add a new node, you just make a new
        class, or subclass, and the class handles the probability table generation

"""

import os
from MarkovifyCustom import Chain
from pathlib import Path
from utils import *
import json
from itertools import accumulate
from pomegranate import *
import numpy as np
from Beat import Beat

BEGIN = "___BEGIN__"
END = "___END__"
CHORD = "CHORD"
MELODYNOTE = "MELODYNOTE"
VOICINGNOTE = "VOICINGNOTE"
NOTECHORD = "NOTECHORD"

DEBUG = False


chord_model_location = Path('./Models/Chord_Model.txt')
melody_note_model_location = Path('./Models/Melody_Note_Model.txt')
voicing_note_model_location = Path('./Models/Voicing_Note_Model.txt')
note_chord_model_location = Path('./Models/Note_Chord_Model.txt')
midifiles_directory = Path("../data/midifiles/")

def log(words):
    if DEBUG:
        print(words)
    else:
        pass


class BayesNet:
    def __init__(self, beat_instance):


        #boolean to control wether or not to read from disk
        self._load_from_disk = False

        self._beat = beat_instance

        self._cond_table_c0 = []
        self._cond_table_c1 = []
        self._cond_table_v0 = []
        self._cond_table_v1 = []
        self._cond_table_m1 = []

        if(self._load_from_disk):
            with open(chord_model_location, 'r') as infile:
                self._chord_model = self._model_from_json(json.load(infile), CHORD)

            with open(melody_note_model_location, 'r') as infile:
                self._melody_note_model = self._model_from_json(json.load(infile), MELODYNOTE)

            with open(note_chord_model_location, 'r') as infile:
                self._note_chord_model = self._model_from_json(json.load(infile), NOTECHORD)

            with open(voicing_note_model_location, 'r') as infile:
                self._voicing_note_model = self._model_from_json(json.load(infile), VOICINGNOTE)

            self._build_alpha_model()

        else:
            self._chord_model = {}
            self._melody_note_model = {}
            self._voicing_note_model = {}
            self._note_chord_model = {}
            self._build_alpha_model()

        
        log("chord model")
        log(self._chord_model)
        if DEBUG: input()
        log("melody note model")
        log(self._melody_note_model)
        if DEBUG: input()
        log("voicing note model")
        log(self._voicing_note_model)
        if DEBUG: input()
        log("note chord model")
        log(self._note_chord_model)
        if DEBUG: input() 

        self._build_cond_table_c0()
        self._build_cond_table_c1()
        self._build_cond_table_v0()
        self._build_cond_table_v1()
        self._build_cond_table_m1()
        self._build_net()


    def _build_alpha_model(self):
        """
            Function: _build_alpha_model

            Description: get song data from every song and build all the models

            Consolidated all the model building to this one function,
            so if we want to add a new network node, we can just edit this
            function, and add probability table generation functions

            NOTE: there could be a key error with the len(keys)-state_size, ie
            the last chord/note may not appear in the keys of the model,
            beware of this
        """
        model = {}
        state_size = 1
        for filename in os.listdir(str(midifiles_directory)):
            if filename.endswith(".mid"):
                beat = Beat(midifiles_directory / filename)
                song_data = get_song_data(beat.midi_file_path, beat.key)
                keys = list(song_data.keys())
                for i in range(len(keys) - state_size):
                    offset = keys[i]
                    item1 = song_data[keys[i]]
                    item2 = song_data[keys[i+state_size]]
                    state = (item1,item2)

                    melody_note = state[0][0]
                    voicing_note = state[0][1]
                    chord = state[0][2]
                    next_melody_note = state[1][0]
                    next_voicing_note = state[1][1]
                    next_chord = state[1][2]

                    if chord is not None and next_chord is not None:
                        if(chord not in self._chord_model):
                            self._chord_model[chord] = {}
                        if(next_chord not in self._chord_model[chord]):
                            self._chord_model[chord][next_chord] = 1
                        else:
                            self._chord_model[chord][next_chord] += 1

                    if melody_note is not None and next_melody_note is not None:
                        if(melody_note not in self._melody_note_model):
                            self._melody_note_model[melody_note] = {}
                        if(next_melody_note not in self._melody_note_model[melody_note]):
                            self._melody_note_model[melody_note][next_melody_note] = 1
                        else:
                            self._melody_note_model[melody_note][next_melody_note] +=1

                    if voicing_note is not None and next_voicing_note is not None:
                        if(voicing_note not in self._voicing_note_model):
                            self._voicing_note_model[voicing_note] = {}
                        if(next_voicing_note not in self._voicing_note_model[voicing_note]):
                            self._voicing_note_model[voicing_note][next_voicing_note] = 1
                        else:
                            self._voicing_note_model[voicing_note][next_voicing_note] += 1

                    if melody_note is not None and chord is not None and next_melody_note is not None \
                    and next_chord is not None:
                        melody_and_chord = melody_note + ',' + chord
                        if(melody_and_chord not in self._note_chord_model):
                            self._note_chord_model[melody_and_chord] = 1
                        else:
                            self._note_chord_model[melody_and_chord] += 1

        #write all models to disk

        with open(chord_model_location, 'w') as outfile:
            json.dump(self._model_to_json(self._chord_model), outfile)

        with open(melody_note_model_location, 'w') as outfile:
            json.dump(self._model_to_json(self._melody_note_model), outfile)

        with open(note_chord_model_location, 'w') as outfile:
            json.dump(self._model_to_json(self._note_chord_model), outfile)

        with open(voicing_note_model_location, 'w') as outfile:
            json.dump(self._model_to_json(self._voicing_note_model), outfile)


    def _build_cond_table_c0(self):
        cond_list = {}
        length = len(self._chord_model.keys())

        for chord, next_chords in self._chord_model.items():
            cond_list[chord] = 1 / length


        self._cond_table_c0 = DiscreteDistribution(cond_list)
        self._all_possible_chords = cond_list.keys()
        self._cond_table_c0 = DiscreteDistribution(cond_list)

        log("c0 cond table")
        log(cond_list)
        if DEBUG: input()


    def _build_cond_table_c1(self):
        cond_list = []
        for chord in self._chord_model:
            choices, weights = zip(*self._chord_model[chord].items())
            total = sum(list(accumulate(weights)))
            for next_chord, count in self._chord_model[chord].items():
                probability = count / total;
                cond_list.append([chord, next_chord, probability])

        #populate all combos that haven't been found with probability 0, pomgranate requires this
        self._fill_in_missing_chord_probabilites(cond_list)

        self._cond_table_c1 = ConditionalProbabilityTable(cond_list, [self._cond_table_c0])

        log("c1 cond table")
        log(cond_list)
        if DEBUG: input()

    def _build_cond_table_v0(self):
        cond_list = {}
        length = len(self._voicing_note_model.keys())
        for note in self._voicing_note_model:
            cond_list[note] = 1 / length

        self._cond_table_v0 = DiscreteDistribution(cond_list)
        self._all_possible_notes = cond_list.keys()

        log("v0 cond table")
        log(cond_list)
        if DEBUG: input()

    def _build_cond_table_v1(self):
        """
            Function: _build_cond_table_v1

            Description: For now this is only V0 and V1, ie there is 
            no dependence on C1, THere should be tho, but its gonna take 
            some time ro write the function that will find v V1 given V0 and C1.
            The problem is none of our song data has such a format. It is only
            chords and a melody note, or voicing and a melody note. I guess I could
            consider the melody note as the voicing but then this node would be similar
            to m1
        """
        cond_list = []
        for note in self._voicing_note_model:
            choices, weights = zip(*self._voicing_note_model[note].items())
            total = sum(list(accumulate(weights)))
            for next_note, count in self._voicing_note_model[note].items():
                probability = count / total;
                cond_list.append([note, next_note, probability])

        self._fill_in_missing_voicing_probabilities(cond_list)
        self._cond_table_v1 = ConditionalProbabilityTable(cond_list, [self._cond_table_v0])

        log("v1 cond table")
        log(cond_list)
        if DEBUG: input()


    def _build_cond_table_m1(self):
        """
            Function: _build_cond_table_m1

            Description: this function builds the conditional probability table for
            the node m1.
        """
        cond_list = []
        total = sum(self._note_chord_model.values())
        for note_chord, count in self._note_chord_model.items():
            note = note_chord.split(',')[0]
            chord = note_chord.split(',')[1]
            probability = count / total
            cond_list.append([chord, note, probability])

        self._fill_in_missing_chord_and_note_probabilites(cond_list)
        self._cond_table_m1 = ConditionalProbabilityTable(cond_list, [self._cond_table_c1])

        log("melody cond table")
        log(cond_list)
        if DEBUG: input()

    def _fill_in_missing_chord_probabilites(self, cond_list):
        data = np.array(cond_list)
        for chord1 in self._all_possible_chords:
            for chord2 in self._all_possible_chords:
                if([chord1, chord2] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord1, chord2, 0.0])

        log("filled in chord cond_list")
        log(cond_list)
    def _fill_in_missing_voicing_probabilities(self, cond_list):
        data = np.array(cond_list)
        for note1 in self._all_possible_notes:
            for note2 in self._all_possible_notes:
                if([note1, note2] in data[:,:2]):
                    continue
                else:
                    cond_list.append([note1, note2, 0.0])

        log("filled in voicing cond_list")
        log(cond_list)

    def _fill_in_missing_chord_and_note_probabilites(self, cond_list):
        data = np.array(cond_list)
        for chord1 in self._all_possible_chords:
            for note1 in self._all_possible_notes:
                if([chord1, note1] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord1, note1, 0.0])

        log("filled in chord and notes")
        log(cond_list)


    def _model_to_json(self, model):
        """
        Dump the chord, note or chord note model as a JSON object, for loading later.
        """
        return json.dumps(list(model.items()))

    def _model_from_json(self, json_thing, kind):
        """
        Given a JSON object or JSON string that was created by `self.to_json`,
        return the corresponding markovify.Chain.
        """
        
        obj = json.loads(json_thing)

        if isinstance(obj, list):
            rehydrated = dict((tuple(item[0]), item[1]) for item in obj)
        elif isinstance(obj, dict):
            rehydrated = obj
        else:
            raise ValueError("Object should be dict or list")

        return rehydrated



    def _build_net(self):
        print("creating nodes")
        v0 = Node(self._cond_table_v0, name="v0")
        v1 = Node(self._cond_table_v1, name="v1")
        c0 = Node(self._cond_table_c0, name="c0")
        c1 = Node(self._cond_table_c1, name="c1")
        m1 = Node(self._cond_table_m1, name="m1")

        print("instantiating network")
        self._bayes_model = BayesianNetwork("Generator")
        print("adding edges")
        self._bayes_model.add_states(v0, c0, m1, v1, c1)
        self._bayes_model.add_edge(c0, c1)
        self._bayes_model.add_edge(v0, v1)
        self._bayes_model.add_edge(c1, m1)

        print("baking model")
        try:
            self._bayes_model.bake()
        except Exception as e:
            print(e)

        print("making prediction")
        log(self._bayes_model.predict(['0', 'I', '4', None, None]))






