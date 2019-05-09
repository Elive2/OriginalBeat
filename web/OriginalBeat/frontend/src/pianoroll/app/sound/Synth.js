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

define(["Tone/core/Tone", "Tone/source/Oscillator", "Tone/instrument/PolySynth", "Tone/instrument/FMSynth", "Tone/effect/JCReverb"],
function (Tone, Oscillator, PolySynth, FMSynth,JCReverb) {



	var Synth = function(){

		this.synth = new PolySynth(8, FMSynth).set({
			"volume" : -22,
			"oscillator" : {
				"type" : "sine1"
			},
			"envelope" : {
				"attack" :  0.01,
				"decay" :  2,
				"sustain" :  1,
				"release" :  4,
			},








		}).toMaster();

        this.reverb = new Tone.JCReverb(.5).set({
            "volume" : -22,
        }).toMaster();

        this.synth.connect(this.reverb);

		this.synth.stealVoices = true;


	};




	Synth.prototype.triggerAttackRelease = function(note, duration, time, vel){
		duration = Math.max(duration, 0.2);
		this.synth.triggerAttackRelease(note, duration, time, vel * 0.5);
	};

	Synth.prototype.releaseAll = function(){
		this.synth.releaseAll();
	};

	return Synth;
});
