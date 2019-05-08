import React from 'react';
import '../index.css';
import { Container, Row, Col} from 'reactstrap';
import InputRoll from './InputRoll'

var CHROMATIC = [ 'C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B' ]

function noteFromMidi(midiNumber) {
  if (isNaN(midiNumber) || midiNumber < 0 || midiNumber > 127) return null;
  var name = CHROMATIC[midiNumber % 12];
  var oct = Math.floor(midiNumber / 12) - 1;
  return name + oct;
}


function formatMidi(midi_json) {
    //console.log("MIDI JSON")
    //console.log(midi_json)
    var formattedHeader = {tempo: 120, timeSignature: [4,4]};
    var formattedNotes = [];

    for(var i = 0; i < midi_json.length; i++) {
        var newNote = {'time': midi_json[i].time.toString() + 'i',
                    'midiNote': midi_json[i].midiNumber,
                    'note': noteFromMidi(midi_json[i].midiNumber),
                    'velocity': 1,
                    'duration': midi_json[i].duration.toString() + 'i',
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

class RollDisplay extends React.Component{
	constructor(props) {
	  super(props);

	  this.state = {
	  	formattedMidi: formatMidi(this.props.data)
	  }
	}

	componentWillReceiveProps() {
		//console.log("PROPS CHANGE")
		//console.log(this.props.data)
		this.setState({
			formattedMidi: formatMidi(this.props.data)
		});
		this.forceUpdate();
	}

	render() {
		return (
      <Row>
        <Col>
            <InputRoll midi={this.state.formattedMidi}/>
        </Col>
      </Row>
		)
	}
}

export default RollDisplay
