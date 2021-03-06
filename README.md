# OriginalBeat

Welcome to The Original Beat github repository

### Overview

The Original Beat is a co-creative web application that helps inspire electronic music producers. The system resembels a Digital Audio Workstation (DAW) in the browser complete with an onscreen piano for the user to input a melody. The system also allows a midi file upload. Then, The Original Beat uses several ML algorithms to generate an accompnaying harmony and drum track that is displayed in a piano roll. The outputted midi file can be downloaded for further modification in the users own DAW. Thorough documentation can be found in the docs folder as well as throughout the codebase.

### Installation

Before installing be sure you have the following:
+ node: >v10.12.0
+ npm: >6.4.1
+ python: >3.6.4

Steps:

1. clone this repository
2. setup and activate a python vitrual environment
3. install python requirements
```
pip3 install -r requirements.txt
```
4. navigate to web/OriginalBeat/frontend then install node modules
```
npm install
```
6. compile jsx files to be coninuously monitored for changes
```
npm run watch
```
7. Set an environment variable PROJ_DIR equal to the root directory of Original Beat on your system
8. navigate back to web start the django dev server
```
python3 manage.py runserver
```
9. visit local host to view the project

for more info and production builds visit the docs folder



### Purpose

This project was completed by Eli Yale, Christian Quintero, and Matt Kordonsky advised by professor Maya Ackerman as part of the Senior Design program at Santa Clara Univeristy for fullfillment of requiremnts for the Computer Science and Engineering B.S. degree. As amateur music enthusiasts, we saw a need for a simple to use in-browser tool to create layered electronic music. We wanted to explore the world of computational creativity and test our knowledge of generative ML algorithms. Please see The Original Beat Conference Presentation Slide deck for more info. The Original Beat Website was live for several months then shutdown in June 2019 due to server costs. The code is preserved here to hopefully inspire others. 

### Tech Used

This is a Django project with a React frontend. We credit Google Chrome Music Lab for their in browser piano roll which we modified with documentation in web/OriginalBeat/frontend/src/pianoroll. We also credit react-piano and SoundFontProvider packages for their in-borwser piano tools. We developed locally with Djagno dev server. Our production server stack included Ubuntu, Djagno, Gunicorn-WSGI, Nginx, Let's Encrypt-ssl, UFW. To implement the musical functions and ML we used the packages Music21, Pomegranate, Tone.js, and MIDI.js. Thank you for checking out our project. Feel free to reach out with any questions.



