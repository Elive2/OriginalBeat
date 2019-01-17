"""
File: CodingGuidelines.py

Description: This file outlines the general coding guidelines we
 follow in this project.

Author: Eli Yale
"""

# Github:
The repo can be found at https://github.com/Elive2/OriginalBeat.git

- Thou shalt always maintain a stable master branch.
- Thou shalt not commit data files or node_modules

# Files:
 Every file should have a block comments as seen above with the name, description, and author.
 All files are commited to git.

# Project Structure:
 The project structure will eveolve over time.

# Documentation:
 We should try and use the pydoc module whenever possible to automate the documentation of our modules.
 To do this simply place a comment between """ """ below functions defenitions, class defenitions, and files.
 The docs can then be accessed with help();
 ie for a class:

class generateMusic():
	"""
		Class: generateMusic

		Description:
			This functions produces beautiful songs. The documentation can be generated with:

				pydoc -w foo

		Author:
			Eli Yale
	"""



# Function Headers:
Include the name of the function, a short description, and any other parts of the codebase
it modifies or effects. Describe each parameter and what the function returns. Remember
Loose Coupling and High Cohesion! see below for an example

def fooBar():
	"""
	Function: fooBar()

	Description: This function makes a sick beat.

	Params: 
	"""
	print(fooBar)


# NOTE: and TODO: and FIXME:
Anytime there is something important to note in the code, go ahead and write NOTE:. This allows
us to quickly scan files for notes. In a simlar way write TODO: anytime there is a task you 
left unfinished. Finally a FIXME: is used to indicate a known bug. I find a todolist at the top of
a file to be useful such as:
[X] - Send midifile to backend
[ ] - Parse Midifile from Frontend



# Packages:

Anytime you add a new package, or change versions be sure to update requirements.txt.
This document is sacred and should always be up to date. I reccomend using a virtual env
so that you can follow the steps below to simply save and install requirements.

pip freeze > requirements.txt
pip install -r requirements.txt

# Coding Style:
