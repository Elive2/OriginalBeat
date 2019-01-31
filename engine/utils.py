import mido
import music21

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