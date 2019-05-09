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

define(["Tone/core/Tone", "Tone/source/Oscillator", "Tone/instrument/PolySynth", "Tone/instrument/AMSynth", "Tone/effect/JCReverb"],
function (Tone, Oscillator, PolySynth, AMSynth,JCReverb) {



	var Bass = function(){

		this.bass = new PolySynth(8, AMSynth).set({
			"volume" : 12,
            "harminoity" : 0.3,
            "oscillator" : {
				"type" : "sine",

			},
			"envelope" : {
				"attack" :  0.01,
				"decay" :  0.4,
				"sustain" :  0.1,
				"release" :  0.46,
			},








		}).toMaster();



		this.bass.stealVoices = true;

        // this.reverb = new Tone.JCReverb(.5).set({
        //     "volume" : -22,
        // }).toMaster();
        //
        // this.bass.connect(this.reverb);

	};




	Bass.prototype.triggerAttackRelease = function(note, duration, time, vel){
		duration = Math.max(duration, 0.2);
		this.bass.triggerAttackRelease(note, duration, time, vel * 0.5);
	};

	Bass.prototype.releaseAll = function(){
		this.bass.releaseAll();
	};

	return Bass;
});
