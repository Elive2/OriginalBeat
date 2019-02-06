import mido
import music21
import mingus
from fractions import Fraction


def findKey(filename):
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

def get_notes_chords_rests(path):
    """
        Function: _get_notes_chords_rests

        Description: Extract into a list all chords, notes, and rests in a midifile
        This looks at only keyboard type insturmnets.

        Parameters:
            path -- (string) absolute file path to a midifile

        Returns: (list) of all events

        NOTE: This expects chords to have their notes played at exactly the same time.
        Offset iterator returns a list of all events that occur at the same offset.
        Will need to do some sort of tolerance snapping cause user inputted melodies
        can't be expected to be right on beat.
    """

    try:
        midi = music21.converter.parse(path)
        parts = music21.instrument.partitionByInstrument(midi)
        #parts.show('text')
        note_list = []
        for music_instrument in range(len(parts)):
            for element_by_offset in music21.stream.iterator.OffsetIterator(parts[music_instrument]):
                for entry in element_by_offset:
                    if isinstance(entry, music21.note.Note):
                        note_list.append(str(entry.pitch))
                    elif isinstance(entry, music21.chord.Chord):
                        note_list.append(' '.join(entry.pitchNames))
                    elif isinstance(entry, music21.note.Rest):
                        note_list.append('R' + str(entry.duration.quarterLength))
        return note_list

    except Exception as e:
        print("failed on ", path, "with exception: ", e)
        pass

def notes_chords_rests_to_midi(song_data):
    s = music21.stream.Stream()
    for note in song_data:
        if (' ' in note):
            event = music21.chord.Chord(note.split(' '))
        elif ('R' in note):
            event = music21.note.Rest()
            event.duration.quarterLength = float(Fraction(note.replace('R','')))
        else:
            event = music21.note.Note(note)

        s.append(event)
        
    mf = music21.midi.translate.streamToMidiFile(s)
    mf.open('../data/output/output1.mid', 'wb')
    mf.write()
    mf.close()




