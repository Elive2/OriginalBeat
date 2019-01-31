"""
    File: crude.py

    Description: This class is a crude generator model but will
    be used as a baseline. It simply generates a chord progression
    staring on the tonic I chord of the the key. Then if uses the hook
    theory API to find the most likely chord that follows. It generates
    a random number and selects the next chord depending on hookthoery
    porbabilities. It is crude because there is no context to the melody

    Author: Eli Yale

    Date Created: January 30, 2018

    NOTES: I am bailing on this model for now, but might be useful later
    Hooktheory just doesn't do what we need. It might be useful if we have several
    chords and need to find the next, but we need to generate chords from scratch
    that will fit the melody and Hooktheory won't help with that

"""

import requests
import json
from numpy.random import choice

url = "https://api.hooktheory.com/v1/trends/nodes"

payload = ""
headers = {
    'Authorization': "Bearer 3056ff41ec3b06f43415302a33be7de1",
    'cache-control': "no-cache",
    'Postman-Token': "42f1032a-0c23-4453-97a2-95bab0723bde"
    }

class Crude():
    """
        Class: Crude

        Description: A very crude generator
    """

    def __init__(self, beatInsatnce):
        self._get_next_chord()


    def _get_next_chord(self,chord=None):
        response = requests.request("GET", url, data=payload, headers=headers)
        response_json = json.loads(response.text)

        probability_distribution = []
        for response_chord_json in response_json[:7]:
            probability_distribution.append(response_chord_json['probability'])

        print(probability_distribution)
        print(sum(self.normalize(probability_distribution)))

        draw = choice(response_json[:7], 1, p=probability_distribution)
        print(draw)

    def normalize(self,probs):
        prob_factor = 1 / sum(probs)
        return [prob_factor * p for p in probs]

