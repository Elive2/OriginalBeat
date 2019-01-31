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

"""

class Crude():
	"""
		Class: Crude

		Description: A very crude generator
	"""

	def __init__(self):
		

