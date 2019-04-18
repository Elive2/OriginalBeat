import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import CSRFToken from './CSRFToken';

var server = "http://127.0.0.1:8000/midi/";


class Upload extends React.Component{
	constructor(props) {
	  super(props);
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
						<Col sm="12" md={{ size: 6, offset: 3 }}>
							<Jumbotron>
								<Form encType="multipart/form-data" action='/midi/' method="post">
								<CSRFToken />
								<Row>
									<Col>
										<FormGroup>
											<Label for="midiFile">Midi File</Label>
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

export default Upload
