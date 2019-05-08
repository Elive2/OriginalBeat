import React from 'react';
import '../index.css';
import '@progress/kendo-theme-default/dist/all.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import {DropDownList} from '@progress/kendo-react-dropdowns';
import Header from './Header';
import Footer from './Footer';
import MelodyRoll from './MelodyRoll'
import HarmonyRoll from './HarmonyRoll'
import DrumRoll from './DrumRoll'
import InstrumentDropdown from './InstrumentDropdown'
import Midi from '@tonejs/midi'

var server = process.env.API_URL

var CHROMATIC = [ 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' ]

function noteFromMidi(midiNumber) {
  if (isNaN(midiNumber) || midiNumber < 0 || midiNumber > 127) return null;
  var name = CHROMATIC[midiNumber % 12];
  var oct = Math.floor(midiNumber / 12) - 1;
  return name + oct;
}

function formatMidi(midi_json) {

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
    // for(var i = 0; i < midi_json['tracks'][1]['notes'].length; i++) {
    //     var oldNote = midi_json['tracks'][1]['notes'][i]
    //     var newNote = {'time': (Math.floor(oldNote['ticks'] / 20)).toString() + 'i',
    //                 'midiNote': oldNote['midi'],
    //                 'note': noteFromMidi(oldNote['midi']),
    //                 'velocity': 1,
    //                 'duration': (Math.floor(oldNote['durationTicks'] / 20)).toString() + 'i',
    //             };
    //     formattedNotes.push(newNote);
    // }
    var formattedMidi = {header: formattedHeader, notes: formattedNotes};

    return formattedMidi;
}

class Project extends React.Component{
	constructor(props) {
	  super(props);
	  // var midiHarmony = Midi.fromUrl(server+'/midi/melody').then(function (data) {
		//   final_mid = formatMidi(data);
	  //
	  // })
	  //
	  // var midiMelody = Midi.fromUrl(server+'/midi/harmony').then(function (data) {
		//   final_mid = formatMidi(data);
	  //
	  //
	  // })
	  //
	  // var midiDrum = Midi.fromUrl(server+'/midi/').then(function (data) {
		//   final_mid = formatMidi(data);
	  //
	  //
	  // })

	  this.state = {
	  	midiMelody: false,
	  	midiHarmony: false,
	  	midiDrum: false
	  };
	  this.melody = {};
	  this.drum = {};
	  this.harmony = {};

	}
	componentDidMount (){
		console.log("project mounted")

		Midi.fromUrl(server+'midi/melody/').then(data => {
			this.setState({
				midiMelody: formatMidi(data)
			})
			// var format = formatMidi(data);
			// console.log(format);
			// this.melody = format;

		 })

		 Midi.fromUrl(server+'midi/harmony/').then(data => {
		 	this.setState({
		 		midiHarmony: formatMidi(data)
		 	})
			//this.harmony = formatMidi(data);


		 })

		 Midi.fromUrl(server+'midi/').then(data => {
		 	this.setState({
		 		midiDrum: formatMidi(data)
		 	})
			//this.drum = formatMidi(data);


		 })
	}

	playAll() {
		var iframe = document.getElementById('melody');
		var innerDoc1 = iframe.contentDocument || iframe.contentWindow.document;
		var iframe = document.getElementById('harmony');
		var innerDoc2 = iframe.contentDocument || iframe.contentWindow.document;
		var iframe = document.getElementById('drum');
		var innerDoc3 = iframe.contentDocument || iframe.contentWindow.document;

    innerDoc1.getElementById('PlayPause').click();
		innerDoc2.getElementById('PlayPause').click();
		innerDoc3.getElementById('PlayPause').click();

     }
	 reSync(){
		document.getElementById('melody').src = document.getElementById('melody').src
		document.getElementById('harmony').src = document.getElementById('harmony').src
		document.getElementById('drum').src = document.getElementById('drum').src

	 }

	 setID(name){
		 document.getElementById('melody').id = name;
	 }


	render() {
		return (
			<div>
				<Header pageSelected={'Project'}/>
				<div class = "title">
					<Row className="layers">
						<Col>

								<Button color="secondary" Style="margin: 10px;"onClick={this.playAll}>Play All</Button>
								<Button color="secondary" onClick={this.reSync}>Re-Sync</Button>



						</Col>

					</Row>

					<Row className="layers">
						<Col xs="4" sm="2" >
							<Row>
								<Col>
									<h3 Style="font-size: 30px;">Original Melody</h3>
								</Col>
							</Row>
							<Row>
								<Col>
									<InstrumentDropdown roll={'melody'}/>
								</Col>
							</Row>
						</Col>
				    	<Col xs="8" sm="8" >

				    		{this.state.midiMelody &&
				    			<MelodyRoll inst={"melody"} midi={this.state.midiMelody}/>
				    		}
								

						</Col>

				  		<Col className="download" sm="2">
							<Form method="get" action="/download/">
								<Button type="submit" color="primary">Download</Button>
							</Form>
						</Col>

					</Row>

					<Row className="layers">
						<Col xs="4" sm="2" >
							<Row>
								<Col>
									<h3 Style="font-size: 30px;">Harmony Layer</h3>
								</Col>
							</Row>
							<Row>
								<Col>
									<InstrumentDropdown roll={'harmony'}/>
								</Col>
							</Row>
						</Col>
						<Col xs="8" sm="8" >

								{this.state.midiHarmony &&
									<MelodyRoll inst={'harmony'} midi={this.state.midiHarmony}/>
								}
								

						</Col>
						<Col className="download" sm="2">
							<Form method="get" action="/download/">
								<Button type="submit" color="primary">Download</Button>
							</Form>
						</Col>
					</Row>

					<Row className="layers">
						<Col xs="4" sm="2" >
							<Row>
								<Col>
									<h3 Style="font-size: 30px;">Drum Layer</h3>
								</Col>
							</Row>
							<Row>
								<Col>
									<InstrumentDropdown roll={'drum'}/>
								</Col>
							</Row>
						</Col>
						<Col xs="8" sm="8" >

								{this.state.midiDrum && 
									<MelodyRoll inst = {'drum'}midi={this.state.midiDrum}/>
								}
								

						</Col>
						<Col className="download" sm="2">
							<Form method="get" action="/download/">
								<Button type="submit" color="primary">Download</Button>
							</Form>
						</Col>
					</Row>
				</div>
				<Footer/>
			</div>
		)
	}
}

export default Project
