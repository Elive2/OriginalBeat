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
				<Header pageSelected={'Home'}/>
					<Row>
						<div className = "title">
							<h4>Original Beat</h4>
						</div>
					</Row>
					<Row>
						<Col sm={{ size: 'auto', offset: 1 }}>
						<Jumbotron>
								Play
								<PianoInput/>
								<br/>
								<img src={"/static/piano.png"} id="piano-img"/>
							</Jumbotron>
						</Col>
						<Col sm={{ size: 'auto', offset: 2 }}>
						<Jumbotron>
								<Form encType="multipart/form-data" action='/midi/' method="post">
								<CSRFToken />
								<Row>
									<Col>
										<FormGroup>
											<Label for="midiFile">Upload</Label>
											<Input type="file" name="Midi" id="midiFile" accept=".mid"/>
											<FormText color="muted">
												Please select a one track midifile to upload
											</FormText>
										</FormGroup>
										<FormGroup>
											<Label for="select_model">Select Generation Model</Label>
											<Input type="select" name="select" id="select_model">
												<option>KeyChord</option>
												<option>KeyChord2</option>
												<option>BayesNet</option>
											</Input>
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
