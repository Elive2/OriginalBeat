```
"""
File: CodingGuidelines.py

Description: This file outlines the general coding guidelines we
 follow in this project.

Author: Eli Yale
"""
```

# Github:
The repo can be found at https://github.com/Elive2/OriginalBeat.git

- Thou shalt always maintain a stable master branch.
- Thou shalt commit early and often
- Thou shalt not commit data files or node_modules or their virtual environment
- Thou shalt use detailed commit messages, explaining exactly what was done

# Files:
 Every file should have a block comments as seen above with the name, description, and author.
 All files are commited to git.

# Project Structure:
 The project structure will eveolve over time. For now, the main generation engine is housed in
 the /engine directory while all frontend and backend code for the web app are housed under the
 /web directory.

# Documentation:
 We should try and use the pydoc module whenever possible to automate the documentation of our modules.
 To do this simply place a comment between """ """ below functions defenitions, class defenitions, and files.
 The docs can then be accessed with help();
 ie for a class:

```
class generateMusic():
	"""
		Class: generateMusic

		Description:
			This functions produces beautiful songs. The documentation can be generated with:

				pydoc -w foo

		Author:
			Eli Yale
	"""
```



# Function Headers:
Include the name of the function, a short description, and any other parts of the codebase
it modifies or effects. Describe each parameter and what the function returns. Remember
Loose Coupling and High Cohesion! see below for an example
```
def fooBar():
	"""
	Function: fooBar()

	Description: This function makes a sick beat.

	Params: 
	"""
	print(fooBar)
```


# NOTE: and TODO: and FIXME:
Anytime there is something important to note in the code, go ahead and write NOTE:. This allows
us to quickly scan files for notes. In a simlar way write TODO: anytime there is a task you 
left unfinished. Finally a FIXME: is used to indicate a known bug. I find a todolist at the top of
a file to be useful such as:

[X] - Send midifile to backend
[ ] - Parse Midifile from Frontend

# Paths in Python:
Do not do hardcode as strings any filepaths used in code.
Instead use os.path.join() or even better, use the pathlib Path object. For example:
```
	from pathlib import Path

	data_folder = Path("source_data/text_files/")

	file_to_open = data_folder / "raw_data.txt"

	f = open(file_to_open)
```



# Packages:

Anytime you add a new package, or change versions be sure to update requirements.txt.
This document is sacred and should always be up to date. I reccomend using a virtual env
so that you can follow the steps below to simply save and install requirements. Please call your
virtual enviornment 'venv', so it can be git ignored.

pip freeze > requirements.txt
pip install -r requirements.txt

# Coding Style:
