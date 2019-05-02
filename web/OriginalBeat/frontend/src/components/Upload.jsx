import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import CSRFToken from './CSRFToken';
import { Piano, KeyboardShortcuts, MidiNumbers } from 'react-piano';
import 'react-piano/dist/styles.css';

var server = process.env.API_URL + "midi/";

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
	}

	

	/*handleSubmit(event) {
  	console.log("HANDLING SUBMIT");
  	//this.toggle()
  	//prevents the default action="" from begin called, instead we handle
  	//the submit in this custom method
  	event.preventDefault();

  	//create an obect which contains all the form data
  	const formData = new FormData(event.target)
  	var formObject = {};
		formData.forEach(function(value, key){
		    formObject[key] = value;
		});

  	//post the FormData object to our backend
  	fetch(server, {
  		method: 'POST',
  		headers: {
  			"Content-Type" : "application/x-www-form-urlencoded",
  		},
  		body: formObject,
  	}).then(response => response.json())
      .then(data => {
      	console.log("UPLOAD SUCCESS")
      });
  }*/

	render() {
		return (
			<div>
				<Header/>
					<Row>
						<div class = "title">
							<h4 class = "font-effect-anaglyph"> Original Beat</h4>
						</div>
					</Row>
					<Row>
						{/*<Col sm="12" md={{ size: 12}}>*/}
						<Col xs="6">
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
						</Col>
						<Col xs="6">
							<Piano noteRange={{first: this.firstNote, last: this.lastNote}}
								playNote={(midiNumber) => {
									//star
									console.log("start")
								}}
								stopNote={(midiNumber) => {
									//stop
									console.log("stop")
								}}
								width={1000}
								keyboardShortcuts={this.keyboardShortcuts}
							/>
						</Col>
					</Row>
				<Footer/>
			</div>
		)
	}
}

export default Upload
