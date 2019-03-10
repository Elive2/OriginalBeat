import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';

class Upload extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Header/>
					<Row>
						<Col sm="12" md={{ size: 6, offset: 3 }}>
							<Jumbotron>
								<Form>
									<FormGroup>
										<Label for="midiFile">Midi File</Label>
										<Input type="file" name="file" id="midiFile" accept=".mid"/>
										<FormText color="muted">
											Please select an 8 bar midifile to upload
										</FormText>
									</FormGroup>
								</Form>
							</Jumbotron>
						</Col>
					</Row>
					<Row>
						<Col sm="12" md={{ size: 6, offset: 3 }}>
							<Button>Submit</Button>
						</Col>
					</Row>
				<Footer/>
			</div>
		)
	}
}

export default Upload
