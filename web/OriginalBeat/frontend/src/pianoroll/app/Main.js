/**
 * Copyright 2016 Google Inc.
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

 /*
    Modifications:

    changes container of roll, interface, and overlay
 */

var server = process.env.API_URL + 'midi/';

var CHROMATIC = [ 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' ]

/**
 * Get the note name (in scientific notation) of the given midi number
 *
 * It uses MIDI's [Tuning Standard](https://en.wikipedia.org/wiki/MIDI_Tuning_Standard)
 * where A4 is 69
 *
 * This method doesn't take into account diatonic spelling. Always the same
 * pitch class is given for the same midi number.
 *
 * @name fromMidi
 * @function
 * @param {Integer} midi - the midi number
 * @return {String} the pitch
 *
 * @example
 * fromMidi(69) // => 'A4'
 */
function noteFromMidi(midiNumber) {
  if (isNaN(midiNumber) || midiNumber < 0 || midiNumber > 127) return null;
  var name = CHROMATIC[midiNumber % 12];
  var oct = Math.floor(midiNumber / 12) - 1;
  return name + oct;
}

function formatMidi(midi_json) {
    //console.log("formating the midi file for pianoroll");

    var formattedHeader = {tempo: 120, timeSignature: [4,4]};
    var formattedNotes = [];

    for(var i = 0; i < midi_json['tracks'][0]['notes'].length; i++) {
        var oldNote = midi_json['tracks'][0]['notes'][i]
        var newNote = {'time': (Math.floor(oldNote['ticks'] / 20)).toString() + 'i',
                    'midiNote': oldNote['midi'],
                    'note': noteFromMidi(oldNote['midi']),
                    'velocity': 1,
                    'duration': (Math.floor(oldNote['durationTicks'] / 20)).toString() + 'i',
                };
        formattedNotes.push(newNote);
    }
    for(var i = 0; i < midi_json['tracks'][1]['notes'].length; i++) {
        var oldNote = midi_json['tracks'][1]['notes'][i]
        var newNote = {'time': (Math.floor(oldNote['ticks'] / 20)).toString() + 'i',
                    'midiNote': oldNote['midi'],
                    'note': noteFromMidi(oldNote['midi']),
                    'velocity': 1,
                    'duration': (Math.floor(oldNote['durationTicks'] / 20)).toString() + 'i',
                };
        formattedNotes.push(newNote);
    }
    var formattedMidi = {header: formattedHeader, notes: formattedNotes};

    return formattedMidi;
}

var final_mid = {};

function init() { window.parent.setUpFrame(); return true; }

function setMidi(midi) {
    final_mid = midi;
}


require(["domready", "roll/Roll", "sound/Player", "interface/Interface", "Tone/core/Transport",
        "midi/preludeInC.json", "StartAudioContext", "style/main.scss", "Tone/core/Tone", "interface/Orientation", "interface/Overlay", "@tonejs/midi"],
    function (domReady, Roll, Player, Interface, Transport, preludeInC,
              StartAudioContext, mainStyle, Tone, Orientation, Overlay, Midi) {

        domReady(function () {

            //the interface
            var player = new Player();

            var roll = new Roll(document.body);

            var interface = new Interface(document.body);

            var overlay = new Overlay(document.body, roll, interface);

            //set the first score
            // const midi = Midi.fromUrl(server).then(function (data) {
            //     //console.log("MIDI NAME");
            //     final_mid = formatMidi(data);
            //     //console.log("FORMATTED MIDI");
            //     //console.log(final_mid);
            //     roll.setScore(final_mid);
            // })
            //console.log(preludeInC);
            roll.setScore(final_mid);

            // fetch(server)
            //   .then(function(response) {
            //     return response.json();
            //   })
            //   .then(function(myJson) {
            //     roll.setScore(myJson);
            //   });

            //roll.setScore(preludeInC);

            /**
             * EVENTS
             */
            interface.onInstrument(function (inst) {
                player.setInstrument(inst);
            });
            interface.onPlay(function (playing) {
                if (playing) {
                    Tone.context.resume();
                    roll.start();
                } else {
                    roll.stop();
                    player.releaseAll();
                }
            });
            interface.onScore(function (json) {
                roll.setScore(json);
            });

            // var wasPlaying = false;
            // interface.onRecord(function (recording) {
            //     if (recording) {
            //         wasPlaying = Transport.state === "started";
            //         roll.stop();
            //     } else {
            //         if (wasPlaying) {
            //             wasPlaying = false;
            //             roll.start();
            //         }
            //     }
            // });
            // interface.onBuffer(function (buffer, duration, onset) {
            //     player.setBuffer(buffer, duration, onset);
            // });


            roll.onnote = function (note, duration, time, velocity) {
                player.triggerAttackRelease(note, duration, time, velocity);
            };
            roll.onstop = function () {
                player.releaseAll();
            };

            var orientation = new Orientation(function () {
                //called when stopped
                Transport.stop();
                roll.stop();
                interface.stop();
            });

            window.parent.postMessage("loaded", "*");

            //send the ready message to the parent
            var isIOS = /iPad|iPhone|iPod/.test(navigator.userAgent) && !window.MSStream;

            //full screen button on iOS
            if (isIOS) {
                //make a full screen element and put it in front
                var iOSTapper = document.createElement("div");
                iOSTapper.id = "iOSTap";
                document.body.appendChild(iOSTapper);
                new StartAudioContext(Tone.context, iOSTapper).then(function() {
                    iOSTapper.remove();
                    window.parent.postMessage('ready', '*');
                });
            } else {
                window.parent.postMessage("ready", "*");
            }

        });
    });
