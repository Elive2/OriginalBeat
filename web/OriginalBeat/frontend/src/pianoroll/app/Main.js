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

var server = "http://127.0.0.1:8000/midi/";

function formatMidi(midi_json) {
    console.log("formating the midi file for pianoroll");

    var formattedHeader = {tempo: 64, timeSignature: [4,4]};
    var formattedNotes = [];

    for(var i = 0; i < midi_json['tracks'][0]['notes'].length; i++) {
        newNote = midi_json['tracks'][0]['notes'][i]
        newNote['velocity'] = 1;
        newNote['noteOffVelocity'] = 1;
        formattedNotes.push(newNote);
    }
    var formattedMidi = {header: formattedHeader, notes: formattedNotes};

    return formattedMidi;
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
            const midi = Midi.fromUrl(server).then(function (data) {
                console.log("MIDI NAME");
                final_mid = formatMidi(data);
                console.log("FORMATTED MIDI");
                console.log(final_mid);
                roll.setScore(final_mid);
            })
            console.log(preludeInC);

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
