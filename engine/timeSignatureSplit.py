import music21
import os

def readTimeSignature(midi_upload_file_path):
    return midi_upload_file_path.ratioString

def main():
    curSong = readTimeSignature('../data/midifiles/HappyBirthday.mid')

if __name__ == '__main__':
    main()
