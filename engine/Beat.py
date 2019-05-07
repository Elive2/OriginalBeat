"""
	File: beat.py

	Description: This file serves holds the beat class.

	Author: Eli Yale
	Date Created: January 23, 2018

"""

class Beat():
	"""
	Class: Beat.py

	Description: Beat is an internal data representation
	of a song in progress. It holds the path to the uploaded
	midi file, the extracted notes, as well as meta data about the
	song. Eventually this class can be serialized and written to disk
	allowing a user to save their song. This class will also be the
	input to the models, allowing us to standardize the input 
	to all models and allow us to hot swap them.

	This class doesn't have any processing methods, only accessors
	and modifiers. Preprocessing is done by the BeatEngine.
	Keep this class as simple as possible with only the data needed
	by the models and project details
	"""

	def __init__(self, midi_upload_file_path, midi_output_file_path):
		self._midi_upload_file_path = midi_upload_file_path
		self._midi_output_file_path = midi_output_file_path

	#getters:

	@property
	def bars(self):
		return self._bars

	@property
	def key(self):
		return self._key

	@property
	def tempo(self):
		return self._tempo

	@property
	def notes_chords_rests(self):
		return self._notes_chords_rests

	@property
	def midi_stream(self):
		return self._midi_stream

	@property
	def midi_stream_melody(self):
		return self._midi_stream_melody

	@property
	def midi_stream_harmony(self):
		return self._midi_stream_harmony
	
	
	@property
	def midi_stream_drums(self):
		return self._midi_stream_drums
	

	@property
	def midi_upload_file_path(self):
		return self._midi_upload_file_path

	@property
	def midi_output_file_path(self):
		return self._midi_output_file_path
	
	
	
	

	#setters:
	#these methods are implemented so that we can later
	#restrict the values set to legal musical values

	@bars.setter
	def bars(self, value):
		self._bars = value

	@key.setter
	def key(self, key):
		self._key = key

	@tempo.setter
	def tempo(self, tempo):
		self._tempo = tempo

	@notes_chords_rests.setter
	def notes_chords_rests(self, data_list):
		self._notes_chords_rests = data_list

	@midi_stream.setter
	def midi_stream(self, stream):
		self._midi_stream = stream

	@midi_stream_melody.setter
	def midi_stream_melody(self, stream):
		self._midi_stream_melody = stream

	@midi_stream_harmony.setter
	def midi_stream_harmony(self, stream):
		self._midi_stream_harmony = stream

	
	@midi_stream_drums.setter
	def midi_stream_drums(self, stream):
		self._midi_stream_drums = stream
	
	
	









