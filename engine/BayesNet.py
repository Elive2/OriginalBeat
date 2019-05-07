"""
    File: BayesNet.py

    Description: This file defines a generator class based on a Bayesian Network

    [ ] - flag to specify to rebuild the chord chain
    [ ] - there has to be a more efficient way to build these probabilites
            with a one pass algorithm. I.E for each event scanned, determine which
            table it applies too, then add it to that tables running cond list and 
            increase the count of that event.
    [x] - functions to fill in missing probabilities
    [x] - rework schema - see notes
    [ ] - if we come across a chord not seen before, add it to the network! ML!
    [ ] - adjust rythm
    [ ] - add in hybrid of Keychord
    [ ] - try to hardcode some better probs


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
import random

BEGIN = "___BEGIN__"
END = "___END__"
CHORD = "CHORD"
MELODYNOTE = "MELODYNOTE"
VOICINGNOTE = "VOICINGNOTE"
NOTECHORD = "NOTECHORD"

POSSIBLE_NOTES = ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']
POSSIBLE_CHORDS = ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']

DEBUG = False


chord_model_location = Path(os.path.join(os.path.join(os.path.join(os.environ['PROJ_DIR'], 'engine'), 'Models'), 'Chord_Model.txt'))
melody_note_model_location = Path(os.path.join(os.path.join(os.path.join(os.environ['PROJ_DIR'], 'engine'), 'Models'), 'Melody_Note_Model.txt'))
voicing_note_model_location = Path(os.path.join(os.path.join(os.path.join(os.environ['PROJ_DIR'], 'engine'), 'Models'), 'Voicing_Note_Model.txt'))
note_chord_model_location = Path(os.path.join(os.path.join(os.path.join(os.environ['PROJ_DIR'], 'engine'), 'Models'), 'Note_Chord_Model.txt'))
midifiles_directory = Path(os.path.join(os.path.join(os.environ['PROJ_DIR'], 'data'), 'midifiles'))
model_output_path = Path(os.path.join(os.path.join(os.path.join(os.environ['PROJ_DIR'], 'engine'), 'Models'), 'Bayes_Net.json'))

# chord_model_location = Path('./Models/Chord_Model.txt')
# melody_note_model_location = Path('./Models/Melody_Note_Model.txt')
# voicing_note_model_location = Path('./Models/Voicing_Note_Model.txt')
# note_chord_model_location = Path('./Models/Note_Chord_Model.txt')
# midifiles_directory = Path("../data/less_midifiles/")
# model_output_path = Path("./Models/Bayes_Net.json")

def log(words):
    if DEBUG:
        print(words)
    else:
        pass


class BayesNet:
    def __init__(self, beat_instance):


        #boolean to control wether or not to read models from disk
        self._load_from_disk = False

        #boolean to control wether to build model manual probabilites,
        #data derived probabilities, or loaded from a json model on disk

        #self._build = 'data'
        self._build = 'disk'
        #self._build = 'manual'

        self._beat = beat_instance

        self._cond_table_c0 = []
        self._cond_table_c1 = []
        self._cond_table_v0 = []
        self._cond_table_v1 = []
        self._cond_table_m1 = []

        self._cond_list_c0 = {}
        self._cond_list_c1 = []
        self._cond_list_v0 = {}
        self._cond_list_v1 = []
        self._cond_list_m1 = []

        if(self._build == 'data'):
            if(self._load_from_disk):
                with open(chord_model_location, 'r') as infile:
                    self._chord_model = self._model_from_json(json.load(infile), CHORD)

                with open(melody_note_model_location, 'r') as infile:
                    self._melody_note_model = self._model_from_json(json.load(infile), MELODYNOTE)

                with open(note_chord_model_location, 'r') as infile:
                    self._note_chord_model = self._model_from_json(json.load(infile), NOTECHORD)

                with open(voicing_note_model_location, 'r') as infile:
                    self._voicing_note_model = self._model_from_json(json.load(infile), VOICINGNOTE)

            else:
                self._chord_model = {}
                self._melody_note_model = {}
                self._voicing_note_model = {}
                self._note_chord_model = {}

            self._init_cond_list_c0()
            self._init_cond_list_c1()
            self._init_cond_list_v0()
            self._init_cond_list_v1()
            self._init_cond_list_m1()

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

        elif(self._build == 'disk'):
            log("loading model from disk")
            with open(model_output_path, 'rb') as f:
                self._bayes_model = BayesianNetwork().from_json(json.load(f))

        elif(self._build == 'manual'):
            self._build_cond_table_c0_manual()
            self._build_cond_table_c1_manual()
            self._build_cond_table_v0_manual()
            self._build_cond_table_v1_manual()
            self._build_cond_table_m1_manual()

            self._build_net()

    def generate(self):
        '''
            self._bayes_model.predict([[v0, c0, m1, None, None]])
        '''

        measure_stream = self._beat.midi_stream.parts[0].makeMeasures(inPlace=False)
        ms = self._beat.midi_stream.parts[0].measures(0,None)

        #c_transposed_part = transpose(self._beat.midi_stream.parts[0], self._beat.key, 'c')
        new_part = music21.stream.Part()


        v1 = ''
        c1 = ''

        #initial notes that will be used to seed the generator
        for measure in ms:
            measure_notes = []
            for note in measure:
                if isinstance(note, music21.note.Note) and v1 == '':
                    v1 = str(note.pitch.pitchClass)
                    measure_notes.append(note.pitch.pitchClass)
                elif (isinstance(note, music21.note.Note)):
                    measure_notes.append(note.pitch.pitchClass)

            chord = music21.chord.Chord(list(set(measure_notes)))
            roman_chord = music21.roman.romanNumeralFromChord(chord, music21.key.Key(self._beat.key))
            c1 = roman_chord.figure
            if(c1 not in POSSIBLE_CHORDS):
                c1 = 'I'

            break


        #simple mechanism to manage the rhythm each entry is the offset that the next
        #harmony note or chord should be played at
        #IDEA: could do this on top of one chord per bar
        rhythm = []

        # #array of all harmony objects to be added to the stream
        # harmony = []

        # for measure in ms:
        #     measureNotes = []
        #     for note in measure:
        #         if isinstance(note, music21.note.Note):
        #             measureNotes.append(note.pitch.pitchClass)

        #     if (len(measureNotes) > 0):
        #         c1 = music21.chord.Chord(list(set(measureNotes)))
        #         #make this a pramter of the time signature
        #         c.duration.quarterLength = 4.0



        for elements_by_offset in music21.stream.iterator.OffsetIterator(self._beat.midi_stream.parts[0]):
            for entry in elements_by_offset:
                log(entry)
                if(isinstance(entry, music21.note.Note)):
                    #first add this entries offset to the rhythm
                    rhythm.append(entry.offset)
                    v0 = v1
                    c0 = c1
                    m1 = str(entry.pitch.pitchClass)

                    prediction = self._bayes_model.predict([[v0,c0,m1,None,None]])
                    v1 = prediction[0][3]
                    c1 = prediction[0][4]

                    chord_list = [str(p) for p in music21.roman.RomanNumeral(c1, self._beat.key).pitches]
                    chord = music21.chord.Chord(chord_list)
                    chord.offset = entry.offset

                    voicing = music21.note.Note()
                    voicing.pitch.pitchClass = int(v1)
                    voicing.offset = entry.offset

                    if(random.randint(0,4) < 3):
                        new_part.append(chord)
                    else:
                        new_part.append(voicing)
            
        self._beat.midi_stream.append(new_part)

        self._beat.midi_stream_harmony = music21.stream.Stream(new_part)

    def predict(self):
        print(self._bayes_model.predict([['0', 'I', '9', None, None]]))



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
                beat = Beat(midifiles_directory / filename, None)
                beat.key = findKey(midifiles_directory / filename)
                song_data = get_song_data(beat.midi_upload_file_path, beat.key)
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
        self._cond_table_c0 = DiscreteDistribution(self._cond_list_c0)

        log("c0 cond table")
        log(self._cond_list_c0)
        if DEBUG: input()


    def _build_cond_table_c1(self):
        for chord in self._chord_model:
            choices, weights = zip(*self._chord_model[chord].items())
            total = sum(list(accumulate(weights)))
            for next_chord, count in self._chord_model[chord].items():
                probability = round(count / total, 2)
                #prevent repitition
                if probability > 0.2:
                    probability = 0.2
                #self._cond_list_c1.append([chord, next_chord, probability])

                index = 0
                for row in self._cond_list_c1:
                    if(row[0] == chord and row[1] == next_chord):
                        log("REPLACING DEFAULT WITH A COMPUTED PROBABILITY")

                        self._cond_list_c1[index] = [chord, next_chord, probability]
                        break

                    index+=1


        self._cond_table_c1 = ConditionalProbabilityTable(self._cond_list_c1, [self._cond_table_c0])

        log("c1 cond table")
        log(self._cond_list_c1)
        if DEBUG: input()

    def _build_cond_table_v0(self):
        self._cond_table_v0 = DiscreteDistribution(self._cond_list_v0)

        log("v0 cond table")
        log(self._cond_list_v0)
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
        for note in self._voicing_note_model:
            choices, weights = zip(*self._voicing_note_model[note].items())
            total = sum(list(accumulate(weights)))
            for next_note, count in self._voicing_note_model[note].items():
                probability = round(count / total, 2)
                #Prevent repitition
                if probability > 0.2:
                    probability = 0.2
                #cond_list.append([note, next_note, probability])

                index = 0
                for row in self._cond_list_v1:
                    if(row[0] == note and row[1] == next_note):
                        log("REPLACING DEFAULT WITH A COMPUTED PROBABILITY")

                        self._cond_list_v1[index] = [note, next_note, probability]
                        break

                    index+=1


        self._cond_table_v1 = ConditionalProbabilityTable(self._cond_list_v1, [self._cond_table_v0])

        log("v1 cond table")
        log(self._cond_list_v1)
        if DEBUG: input()


    def _build_cond_table_m1(self):
        """
            Function: _build_cond_table_m1

            Description: this function builds the conditional probability table for
            the node m1.
        """
        total = sum(self._note_chord_model.values())
        for note_chord, count in self._note_chord_model.items():
            note = note_chord.split(',')[0]
            chord = note_chord.split(',')[1]
            probability = round(count / total, 2)
            #cond_list.append([chord, note, probability])

            index = 0
            for row in self._cond_list_m1:
                if(row[0] == chord and row[1] == note):
                    log("REPLACING DEFAULT WITH A COMPUTED PROBABILITY")

                    self._cond_list_m1[index] = [chord, note, probability]
                    break

                index+=1

        self._cond_table_m1 = ConditionalProbabilityTable(self._cond_list_m1, [self._cond_table_c1])

        log("melody cond table")
        log(self._cond_list_m1)
        if DEBUG: input()

    def _init_cond_list_c0(self):
        self._cond_list_c0 = {}
        for chord in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            self._cond_list_c0[chord] = 1 / 12

    def _init_cond_list_c1(self):
                #Note: should preallocate this and not append
        self._cond_list_c1 = []
        for chord1 in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            for chord2 in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
                prob = 0.0
                self._cond_list_c1.append([chord1, chord2, prob])

    def _init_cond_list_v0(self):
        self._cond_list_v0 = {}
        for note in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
            self._cond_list_v0[note] = 1 / 12

    def _init_cond_list_v1(self):
        self._cond_list_v1 = []
        for note1 in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
            for note2 in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
                prob = 0.0
                self._cond_list_v1.append([note1, note2, prob])

    def _init_cond_list_m1(self):
        self._cond_list_m1 = []
        for chord in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            for note in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
                prob = 0.0
                self._cond_list_m1.append([chord, note, prob])


    '''
        The following methods are preserved for legacy sake
    '''
    def _build_cond_table_c0_manual(self):
        self._cond_list_c0 = {}
        for chord in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            cond_list[chord] = 1 / 12

        if(DEBUG):
            print("c0 cond_list")
            print(cond_list)
            input()

        self._cond_table_c0 = DiscreteDistribution(self._cond_list_c0)


    def _build_cond_table_c1_manual(self):
                #Note: should preallocate this and not append
        self._cond_list_c1 = []
        for chord1 in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            for chord2 in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
                prob = random.uniform(0,1)
                cond_list.append([chord1, chord2, prob])

        if(DEBUG):
            print("c1 cond list")
            print(cond_list)
            input()

        self._cond_table_c1 = ConditionalProbabilityTable(self._cond_list_c1, [self._cond_table_c0])

    def _build_cond_table_v0_manual(self):
        self._cond_list_v0 = {}
        for note in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
            cond_list[note] = 1 / 12

        self._cond_table_v0 = DiscreteDistribution(self._cond_list_v0)

        if(DEBUG):
            print("vo cond list")
            print(cond_list)
            input()


    def _build_cond_table_v1_manual(self):
        self._cond_list_v1 = []
        for note1 in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
            for note2 in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
                prob = random.uniform(0,1)
                cond_list.append([note1, note2, prob])

        self._cond_table_v1 = ConditionalProbabilityTable(cond_list, [self._cond_table_v0])

        if(DEBUG):
            print("v1 cond list")
            print(cond_list)
            input()

    def _build_cond_table_m1_manual(self):
        self._cond_list_m1 = []
        for chord in ['i' ,'ii', 'iii', 'iv', 'v', 'vi', 'I', 'II', 'III', 'IV', 'V', 'VI']:
            for note in ['0', '1', '2', '3', '4','5','6','7','8','9','10','11']:
                prob = random.uniform(0,1)
                cond_list.append([chord, note, prob])

        self._cond_table_m1 = ConditionalProbabilityTable(cond_list, [self._cond_table_c1])

        if(DEBUG):
            print("m1 cond list")
            print(cond_list)
            input()

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
        log("creating nodes")
        v0 = Node(self._cond_table_v0, name="v0")
        v1 = Node(self._cond_table_v1, name="v1")
        c0 = Node(self._cond_table_c0, name="c0")
        c1 = Node(self._cond_table_c1, name="c1")
        m1 = Node(self._cond_table_m1, name="m1")

        log("instantiating network")
        self._bayes_model = BayesianNetwork("Generator")
        log("adding edges")
        self._bayes_model.add_nodes(v0, c0, m1, v1, c1)
        self._bayes_model.add_edge(c0, c1)
        self._bayes_model.add_edge(v0, v1)
        self._bayes_model.add_edge(c1, m1)

        log("baking model")
        try:
            self._bayes_model.bake()
        except Exception as e:
            print(e)

       #self._bayes_model.plot()
        log("saving model to disk")
        with open(model_output_path, 'w') as f:
            json.dump(self._bayes_model.to_json(), f)

        # print("making prediction")
        # print(self._bayes_model.predict([['5', 'iii', '4', None, None]]))
        # print("making prediction")
        # print(self._bayes_model.predict([['0', 'ii', '4', None, None]]))
        # print("making prediction")
        # print(self._bayes_model.predict([['0', 'I', '4', None, None]]))
        # print("making prediction")
        # print(self._bayes_model.predict([['4', 'I', '4', None, None]]))
        # print("making prediction")
        # print(self._bayes_model.predict([['0', 'v', '4', None, None]]))


