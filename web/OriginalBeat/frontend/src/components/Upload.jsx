import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import CSRFToken from './CSRFToken';
import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano';
import 'react-piano/dist/styles.css';
import posed, {PoseGroup} from 'react-pose';
import DimensionsProvider from './DimensionsProvider';
import SoundfontProvider from './SoundfontProvider';

var server = process.env.API_URL + "midi/";

const WonkyModal = posed.div({
	fullscreen: {
		width: "100vw",
		height: "100vh",
		transition: {
		  duration: 400,
		  ease: 'linear'
		}
	},
	idle: {
		width: "100%",
		height: "100%",
		transition: {
		  duration: 400,
		  ease: 'linear'
		}
	},
	invisible: {
		applyAtEnd: { display: "none" },
	}
})

// webkitAudioContext fallback needed to support Safari
const audioContext = new (window.AudioContext || window.webkitAudioContext)();
const soundfontHostname = 'https://d1pzp51pvbm36p.cloudfront.net';

const noteRange = {
  first: MidiNumbers.fromNote('c3'),
  last: MidiNumbers.fromNote('f5'),
};
const keyboardShortcuts = KeyboardShortcuts.create({
  firstNote: noteRange.first,
  lastNote: noteRange.last,
  keyboardConfig: KeyboardShortcuts.HOME_ROW,
});

class Upload extends React.Component{
	constructor(props) {
	  super(props);

	  this.firstNote = MidiNumbers.fromNote('c3')
	  this.lastNote = MidiNumbers.fromNote('f5')
	  this.keyboardShortcuts = KeyboardShortcuts.create({
	  	firstNote: this.firstNote,
	  	lastNote: this.lastNote,
	  	keyboardConfig: KeyboardShortcuts.HOME_ROW,
	  })
	  this.state = {
	  	uploadPose: 'idle',
	  	pianoPose: 'idle',
	  }
	}

  selectMethod(method) {
  	if(method == 'upload') {
  		this.setState({
  			uploadPose: 'fullscreen',
  			pianoPose: 'invisible'
  		})
  	}
  	else if(method == 'piano') {
  		this.setState({
  			pianoPose: 'fullscreen',
  			uploadPose: 'invisible'
  		})
  	}

  }


	render() {
		return (
			<div>
				<Header pageSelected={'Home'}/>
					<Row>
						<div class = "title">
							<h4 class = "font-effect-anaglyph"> Original Beat</h4>
						</div>
					</Row>
					<Row>
						<Col sm="6">
						<WonkyModal className="wonkyModal" id="pianoBox" pose={this.state.pianoPose} onClick={() => this.selectMethod('piano')}>
									<DimensionsProvider>
							      {({ containerWidth, containerHeight }) => (
							        <SoundfontProvider
							          instrumentName="acoustic_grand_piano"
							          audioContext={audioContext}
							          hostname={soundfontHostname}
							          render={({ isLoading, playNote, stopNote }) => (
							            <Piano
							              noteRange={noteRange}
							              width={containerWidth}
							              playNote={playNote}
							              stopNote={stopNote}
							              disabled={isLoading}
							              keyboardShortcuts={keyboardShortcuts}
							              {...this.props}
							            />
							          )}
							        />
							      )}
							    </DimensionsProvider>
						</WonkyModal>
						</Col>
						<Col sm="6">
						<WonkyModal className="wonkyModal" id="pianoBox" pose={this.state.uploadPose} onClick={() => this.selectMethod('upload')}>
							<Jumbotron>
								<Form encType="multipart/form-data" action='/midi/' method="post">
								<CSRFToken />
								<Row>
									<Col>
										<FormGroup>
											<Label for="midiFile">To begin please upload a midi file below</Label>
											<Input type="file" name="Midi" id="midiFile" accept=".mid"/>
											<FormText color="muted">
												Please select an 9 bar midifile to upload
											</FormText>
										</FormGroup>
									</Col>
								</Row>
								<Row>
									<Col>
										<Button type="submit">Submit</Button>
									</Col>
								</Row>
							</Form>
							</Jumbotron>
							</WonkyModal>
						</Col>
					</Row>
				<Footer/>
			</div>
		)
	}
}

export default Upload
