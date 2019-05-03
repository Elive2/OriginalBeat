import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import CSRFToken from './CSRFToken';
import PianoInput from './PianoInput';

var server = process.env.API_URL + "midi/";




class Upload2 extends React.Component{
	constructor(props) {
	  super(props);
	}

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
						<Col sm="6">
						<Jumbotron>
								<PianoInput />
							</Jumbotron>
						</Col>
						<Col sm="6">
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
					</Row>
				<Footer/>
			</div>
		)
	}
}

export default Upload2
