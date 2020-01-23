```
"""
File: WebAppNotes.md

Description: This file documents the web app for Original Beat

Author: Eli Yale
"""
```

# Github:
The repo can be found at https://github.com/Elive2/OriginalBeat.git

# Files:
all files related to the frontend and back end can be found in the /web directory

# Directory Structure
Since we combine a django app with a React frontend our directory structure is slightly complicated.
The /web directory is technically a Django project and each sub directory is a Django App. For now we
just have the main /web/mysite app which is similar to the Django Turotrial and the /web/OriginalBeat app which
contains most of the code for displaying the main website. /web/mysite only contains some base url patterns
to reference OriginalBeat as well as the seetings.py file.

Inside /web/OriginalBeat you find all the frontend react code including config files in the /web/OrigianlBeat/frontned directory.
All static js files, images, and static html files are found in the /static directory. Django will serve static
files from this directory. All server rendered html files are in the /web/OrigianlBeat/templates/OriginalBeat directory.

Inside /web/OrigianlBeat/frontend you will find all source .jsx files in src. For info about the commands to
build the project see the Useful Commands Section

# Useful Commands

1. To compile all frontend .jsx files:
navigate to /web/OriginalBeat/frontend and run

```
npm run watch
```

This command will compile and bundle the frontend placing the output in the /web/OrigianlBeat/static/bundles folder
as well as continuous watch for changes to any js files and recompile automatically

2. To Compile the PianoRoll from Google Creative Lab
navigate to /web/OriginalBeat/frontend/src/pianoroll and run

```
npm run build
```

This command will compile once the piano roll and place all necssary files in the /web/OrigianlBeat/static/ folder

3. To serve the files and run the app
navigate to /web and run

```
python3 manage.py runserver
```

and visit http://127.0.0.1:8000/OriginalBeat/

4. **_deprecated_** To do a production build for our old DigitalOcean server navigate to /web and run

```
npm run prod
```


