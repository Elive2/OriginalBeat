import mido
import music21
import mingus
from fractions import Fraction

#NOTE: IT may be faster to parse the midifile once then pass
#the stream object to these functions

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

def get_chords(path):
    """
        Function: get_chords

        Description: Extrcact into a list all the chords in a song, if there is
        no chord with Note-ons associated with an melody note, the chord is None.
        This function uses the chordify method from music 21 to make everything
        in the song into chords. This helps with songs that are sparsely chorded.
        This function also elimates duplicate notes from chords as there
        would be way too many

        Parameters:
            path -- (string) absolute file path to a midifile

        Returns:  (list) of a all chord events

        //this method parses all the notes together into chords, could be useful
        s = midi.chordify()

    """
    midi = music21.converter.parse(path)
    midi_chords = midi.chordify()

    chord_list = []
    for element_by_offset in music21.stream.iterator.OffsetIterator(midi_chords):
        for entry in element_by_offset:
            if isinstance(entry, music21.chord.Chord):
                chord = [str(e) for e in set(entry.pitchClasses)]
                if(len(chord) > 1):
                    chord_list.append(','.join(chord))

    return chord_list

def get_notes(path):
    """
        Function: get_notes

        Desription: Extract into a list all the notes in a song.

        Return: (list) of all note events as strings
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
                        note_list.append(str(entry.pitch.pitchClass))

        return note_list

    except Exception as e:
        print("failed on ", path, "with exception: ", e)
        pass


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

def get_simul_chords_and_notes(path):
    """
        Function: get_simul_chords_and_notes

        Desription: Extract into all melody notes that play at the same time
        as a chord

        Return: (list) of all simulatenous notes and chord events as strings
        There may be more than one note associated with the chord, in that case
        they would be space sepearted
        of the format: 'note, chord' ie 'c4, 0 1 5' or 'c4 c5, 0 1 5'
    """
    midi = music21.converter.parse(path)
    parts = music21.instrument.partitionByInstrument(midi)
    chord_and_note_list = []
    part = parts[1] if len(parts) > 1 else parts[0]
    try:
        for element_by_offset in music21.stream.iterator.OffsetIterator(part):
            #print(element_by_offset)
            for entry in element_by_offset:
                #print(entry)
                if isinstance(entry, music21.chord.Chord):
                    chord = [str(e) for e in entry.pitchClasses]

                    #the below line works ok, but I think It includes all sounds that are still echoing??
                    melodyNotes = parts[0].allPlayingWhileSounding(entry, part).notes
                    note_list = []
                    for note in melodyNotes:
                        if(isinstance(note , music21.note.Note)):
                            note_list.append(str(note.pitch.pitchClass))

                    if(len(chord) > 1 and len(note_list) > 0):
                        chord_and_note_list.append((list(set(note_list)), chord))
                        #chord_and_note_list.append(' '.join(note_list) + ', ' +' '.join(chord))
    except Exception as e:
        print(e)
        return []

    return chord_and_note_list

def get_song_data(path, given_key):
    """
        Function: get_song_data
    
        Description: Get all song event and categorize by offset. The returned data
        structure has format:
        {
            offset1: [melody_note, voicing_note, chord]
            offset2: [melody_note, voicing_note, chord]
            offset3: [melody_note, voicing_note, chord]
        }
        if any of the note or chords are not found at the offset, they have value None
        should everything be transposed to c? including melody?
    """

    try:

        midi = music21.converter.parse(path)
        parts = music21.instrument.partitionByInstrument(midi)
        song_data = {}

        chord_part = parts[1] if len(parts) > 1 else parts[0]
        melody_part = parts[0]
        voicing_part = melody_part

        #loop through elements in the melody part
        for elements_by_offset in music21.stream.iterator.OffsetIterator(melody_part):
            melody_note = None
            voicing_note = None
            chord = None
            for entry in elements_by_offset:
                offset = entry.offset

                if isinstance(entry, music21.chord.Chord):
                    #if its a chord, (unlikely) add it as a chord
                    if(len(entry.pitchClasses) > 1):
                        #chord_notes = ' '.join([str(e) for e in entry.name])
                        chord = music21.roman.romanNumeralFromChord(entry, music21.key.Key(given_key)).romanNumeralAlone
                    else:
                        voicing_note = str(entry.pitch.pitchClass)
                elif isinstance(entry, music21.note.Note):
                    #if it is a melody note, add the melody note to the data
                    melody_note = str(entry.pitch.pitchClass)

                    #find all chords or voicings that are sounding at the same time in the chord/voicing part
                    sounding = chord_part.allPlayingWhileSounding(entry, melody_part)
                    for sounding_note in sounding:
                        if isinstance(sounding_note, music21.chord.Chord):
                                chord = music21.roman.romanNumeralFromChord(sounding_note, music21.key.Key(given_key)).romanNumeralAlone
                        elif isinstance(sounding_note, music21.note.Note):
                            voicing_note = str(sounding_note.pitch.pitchClass)

                        #can't handle the case if there are multiple chords sounding
                else:
                    continue

                song_data[offset] = [melody_note, voicing_note, chord]

        #print("got song data")
        return song_data

    except Exception as e:
        print("failed on path " + str(path) + " with error: ")
        print(e)

def transpose(part, from_key, to_key):
    i = interval.Interval(from_key.tonic, pitch.Pitch(to_key))
    return part.transpose(i)

def notes_chords_rests_to_midi(song_data):
    s = music21.stream.Stream()
    for note in song_data:
        if (' ' in note):
            event = music21.chord.Chord(note.split(' '))
        elif ('R' in note):
            continue
            event = music21.note.Rest()
            event.duration.quarterLength = float(Fraction(note.replace('R','')))
        else:
            event = music21.note.Note(note)

        s.append(event)

    mf = music21.midi.translate.streamToMidiFile(s)
    mf.open('../data/output/output1.mid', 'wb')
    mf.write()
    mf.close()




