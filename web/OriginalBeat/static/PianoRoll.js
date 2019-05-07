/******/ (function(modules) { // webpackBootstrap
/******/ 	// install a JSONP callback for chunk loading
/******/ 	var parentJsonpFunction = window["webpackJsonp"];
/******/ 	window["webpackJsonp"] = function webpackJsonpCallback(chunkIds, moreModules) {
/******/ 		// add "moreModules" to the modules object,
/******/ 		// then flag all "chunkIds" as loaded and fire callback
/******/ 		var moduleId, chunkId, i = 0, callbacks = [];
/******/ 		for(;i < chunkIds.length; i++) {
/******/ 			chunkId = chunkIds[i];
/******/ 			if(installedChunks[chunkId])
/******/ 				callbacks.push.apply(callbacks, installedChunks[chunkId]);
/******/ 			installedChunks[chunkId] = 0;
/******/ 		}
/******/ 		for(moduleId in moreModules) {
/******/ 			if(Object.prototype.hasOwnProperty.call(moreModules, moduleId)) {
/******/ 				modules[moduleId] = moreModules[moduleId];
/******/ 			}
/******/ 		}
/******/ 		if(parentJsonpFunction) parentJsonpFunction(chunkIds, moreModules);
/******/ 		while(callbacks.length)
/******/ 			callbacks.shift().call(null, __webpack_require__);

/******/ 	};

/******/ 	// The module cache
/******/ 	var installedModules = {};

/******/ 	// object to store loaded and loading chunks
/******/ 	// "0" means "already loaded"
/******/ 	// Array means "loading", array contains callbacks
/******/ 	var installedChunks = {
/******/ 		0:0
/******/ 	};

/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {

/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId])
/******/ 			return installedModules[moduleId].exports;

/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			exports: {},
/******/ 			id: moduleId,
/******/ 			loaded: false
/******/ 		};

/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);

/******/ 		// Flag the module as loaded
/******/ 		module.loaded = true;

/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}

/******/ 	// This file contains only the entry chunk.
/******/ 	// The chunk loading function for additional chunks
/******/ 	__webpack_require__.e = function requireEnsure(chunkId, callback) {
/******/ 		// "0" is the signal for "already loaded"
/******/ 		if(installedChunks[chunkId] === 0)
/******/ 			return callback.call(null, __webpack_require__);

/******/ 		// an array means "currently loading".
/******/ 		if(installedChunks[chunkId] !== undefined) {
/******/ 			installedChunks[chunkId].push(callback);
/******/ 		} else {
/******/ 			// start chunk loading
/******/ 			installedChunks[chunkId] = [callback];
/******/ 			var head = document.getElementsByTagName('head')[0];
/******/ 			var script = document.createElement('script');
/******/ 			script.type = 'text/javascript';
/******/ 			script.charset = 'utf-8';
/******/ 			script.async = true;

/******/ 			script.src = __webpack_require__.p + "../../../static/" + chunkId + ".js";
/******/ 			head.appendChild(script);
/******/ 		}
/******/ 	};

/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;

/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;

/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";

/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(0);
/******/ })
/************************************************************************/
/******/ ([
/* 0 */
/***/ (function(module, exports, __webpack_require__) {

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

	var server = ("https://138.197.199.250/") + 'midi/';

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

	__webpack_require__.e/* require */(1, function(__webpack_require__) { var __WEBPACK_AMD_REQUIRE_ARRAY__ = [__webpack_require__(1), __webpack_require__(2), __webpack_require__(29), __webpack_require__(79), __webpack_require__(5),
	        __webpack_require__(85), __webpack_require__(86), __webpack_require__(87), __webpack_require__(6), __webpack_require__(89), __webpack_require__(90), __webpack_require__(94)]; (function (domReady, Roll, Player, Interface, Transport, preludeInC,
	              StartAudioContext, mainStyle, Tone, Orientation, Overlay, Midi) {

	        domReady(function () {

	            //the interface
	            var player = new Player();

	            var roll = new Roll(document.body);

	            var interface = new Interface(document.body);

	            var overlay = new Overlay(document.body, roll, interface);

	            //set the first score
	            const midi = Midi.fromUrl(server).then(function (data) {
	                //console.log("MIDI NAME");
	                final_mid = formatMidi(data);
	                //console.log("FORMATTED MIDI");
	                //console.log(final_mid);
	                roll.setScore(final_mid);
	            })
	            //console.log(preludeInC);

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
	    }.apply(null, __WEBPACK_AMD_REQUIRE_ARRAY__));});


/***/ })
/******/ ]);