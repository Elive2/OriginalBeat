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

"""

import os
from MarkovifyCustom import Chain
from pathlib import Path
from utils import *
import json
from itertools import accumulate
from pomegranate import *
import numpy as np

BEGIN = "___BEGIN__"
END = "___END__"

chord_chain_location = Path('./Models/Chord_Chain.txt')
note_chain_location = Path('./Models/Note_Chain.txt')
midifiles_directory = Path("../data/midifiles/")

class BayesNet:
    def __init__(self, beat_instance):
        self._note_corpus = []
        self._chord_corpus = []

        self._cond_table_c0 = []
        self._cond_table_c1 = []
        self._cond_table_v0 = []
        self._cond_table_v1 = []
        self._cond_table_m1 = []

        with open(chord_chain_location, 'r') as infile:
            self._chord_chain = Chain.from_json(json.load(infile))

        with open(note_chain_location, 'r') as infile:
            self._note_chain = Chain.from_json(json.load(infile))

        # self._chord_chain = self._build_chord_chain()
        # self._note_chain = self._build_note_chain()
        self._m1_model = self._build_m1_model()

        self._beat = beat_instance
        self._build_cond_table_c0()
        self._build_cond_table_c1()
        self._build_cond_table_v0()
        self._build_cond_table_v1()
        self._build_cond_table_m1()
        self._build_net()


    def _build_chord_chain(self):
        for filename in os.listdir(str(midifiles_directory)):
            if filename.endswith(".mid"): 
                path = midifiles_directory / filename
                song_data = get_chords(path)
                self._chord_corpus.append(song_data)
                continue
            else:
                continue

        #build a markov chain of the chord, state size one
        #this will help compute the probability table
        the_chain = Chain(self._chord_corpus, 1)

        with open(chord_chain_location, 'w') as outfile:
            json.dump(the_chain.to_json(), outfile)

        return the_chain

    def _build_note_chain(self):
        for filename in os.listdir(str(midifiles_directory)):
            if filename.endswith(".mid"): 
                path = midifiles_directory / filename
                song_data = get_notes(path)
                self._note_corpus.append(song_data)
                continue
            else:
                continue

        #build a markov chain of the notes, state size one
        #this will help compute the probability table
        the_chain = Chain(self._note_corpus, 1)

        with open(note_chain_location, 'w') as outfile:
            json.dump(the_chain.to_json(), outfile)

        return the_chain

    def _build_m1_model(self):
        """
            Function: _build_m1_model

            Description: we can't use a markov model for simultaneous
            notes and chords because it is not a discrete time
            markov process. So instead just build a custom model. It 
            is simply a dictionary where the keys are the possible
            note-chord combonations and the value is the count of occurnces
            in the data. Its might look something like this 

            {
                "C4, 0 3 5":12
                "C#4, 1 4":9

            }
        """
        model = {}
        for filename in os.listdir(str(midifiles_directory)):
            if filename.endswith(".mid"):
                path = midifiles_directory / filename
                song_data = get_simul_chords_and_notes(path)
                for pair in song_data:
                    for possible_note in pair[0]:
                        data_string = possible_note + ', ' + ' '.join(pair[1])
                    if(data_string not in model):
                        model[data_string] = 1;
                    else:
                        model[data_string] += 1;

        return model

    def _build_cond_table_c0(self):
        cond_list = {}
        length = len(self._chord_chain.model.keys())

        for chord, next_chords in self._chord_chain.model.items():
            if(chord == BEGIN or chord == END or chord == (BEGIN)):
                continue
            cond_list[chord[0]] = 1 / length

        self._cond_table_c0 = DiscreteDistribution(cond_list)
        self._all_possible_chords = cond_list.keys()

        # print(cond_list)
        # input()

    def _build_cond_table_c1(self):
        cond_list = []
        for chord in self._chord_chain.model:
            choices, weights = zip(*self._chord_chain.model[chord].items())
            total = sum(list(accumulate(weights)))
            for next_chord in self._chord_chain.model[chord].items():
                probability = next_chord[1] / total;
                cond_list.append([chord[0], next_chord[0], probability])

        #populate all combos that haven't been found with probability 0, pomgranate requires this
        self._fill_in_missing_chord_probabilites(cond_list)

        self._cond_table_c1 = ConditionalProbabilityTable(cond_list, [self._cond_table_c0])

        # print(cond_list)
        # input()


    def _build_cond_table_v0(self):
        cond_list = {}
        length = len(self._note_chain.model.keys())
        for note in self._note_chain.model:
            #cond_list.append([note, 1 / length])
            cond_list[note[0]] = 1 / length

        self._cond_table_v0 = DiscreteDistribution(cond_list)
        self._all_possible_notes = cond_list.keys()

        # print(cond_list)
        # input()

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
        for note in self._note_chain.model:
            choices, weights = zip(*self._note_chain.model[note].items())
            total = sum(list(accumulate(weights)))
            for next_note in self._note_chain.model[note].items():
                probability = next_note[1] / total;
                cond_list.append([note[0], next_note[0], probability])

        # print(cond_list)
        # input()
        self._fill_in_missing_voicing_probabilities(cond_list)
        self._cond_table_v1 = ConditionalProbabilityTable(cond_list, [self._cond_table_v0])


    def _build_cond_table_m1(self):
        """
            Function: _build_cond_table_m1

            Description: this function build the conditional probability table for
            the node m1.
        """
        cond_list = []
        total = sum(self._m1_model.values())
        for note_chord in self._m1_model:
            note = note_chord.split(', ')[0]
            chord = ','.join(note_chord.split(', ')[1].split(' '))
            probability = self._m1_model[note_chord] / total
            cond_list.append([chord, note, probability])

        # print(cond_list)
        # input()
        # print(self._cond_table_c1)
        # input()

        self._fill_in_missing_chord_and_note_probabilites(cond_list)
        self._cond_table_m1 = ConditionalProbabilityTable(cond_list, [self._cond_table_c1])

    def _fill_in_missing_chord_probabilites(self, cond_list):
        data = np.array(cond_list)
        for chord1 in self._all_possible_chords:
            for chord2 in self._all_possible_chords:
                if([chord1, chord2] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord1, chord2, 0.0])

    def _fill_in_missing_voicing_probabilities(self, cond_list):
        data = np.array(cond_list)
        for note1 in self._all_possible_notes:
            for note2 in self._all_possible_notes:
                if([note1, note2] in data[:,:2]):
                    continue
                else:
                    cond_list.append([note1, note2, 0.0])

    def _fill_in_missing_chord_and_note_probabilites(self, cond_list):
        data = np.array(cond_list)
        for chord1 in self._all_possible_chords:
            for note1 in self._all_possible_notes:
                if([chord1, note1] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord1, note1, 0.0])

        for note_chord1 in self._m1_model:
            for note_chord2 in self._m1_model:
                print(note_chord1)
                print(note_chord2)
                note1 = note_chord1.split(', ')[0]
                chord1 = ','.join(note_chord1.split(', ')[1].split(' '))
                note2 = note_chord2.split(', ')[0]
                chord2 = ','.join(note_chord2.split(', ')[1].split(' '))
                print(note1)
                print(note2)
                print(chord1)
                print(chord2)
                input()
                if([chord1, note1] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord1, note1, 0.0])
                if([chord1, note2] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord1, note2, 0.0])
                if([chord2, note1] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord2, note1, 0.0])
                if([chord2, note2] in data[:,:2]):
                    continue
                else:
                    cond_list.append([chord2, note2, 0.0])





    def _build_net(self):
        v0 = Node(self._cond_table_v0, name="v0")
        v1 = Node(self._cond_table_v1, name="v1")
        c0 = Node(self._cond_table_c0, name="c0")
        c1 = Node(self._cond_table_c1, name="c1")
        m1 = Node(self._cond_table_m1, name="m1")

        self._bayes_model = BayesianNetwork("Generator")
        self._bayes_model.add_states(v0, c0, m1, v1, c1)
        self._bayes_model.add_edge(c0, c1)
        self._bayes_model.add_edge(v0, v1)
        self._bayes_model.add_edge(c1, m1)

        self._bayes_model.bake()

        print(self._bayes_model.predict(['B-', '5,10,2', 'F', None, None]))






