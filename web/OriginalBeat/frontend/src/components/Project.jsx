import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import MelodyRoll from './MelodyRoll'
import HarmonyRoll from './HarmonyRoll'
import DrumRoll from './DrumRoll'




class Project extends React.Component{
	constructor(props) {
	  super(props);
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

	render() {
		return (
			<div>
				<Header/>
				<div class = "title">
					<Row>
						<Col>

								<Button color="secondary" onClick={this.playAll}>Play All</Button>

						</Col>
					</Row>

					<Row>
						<Col xs="4" sm="2" ></Col>
				    	<Col xs="8" sm="8" >

								<h3>Original Melody</h3>

								<MelodyRoll/>
								<Form method="get" action="/download/">
								<Button id="ddd" type="submit" color="primary">Download</Button>
								</Form>

						</Col>
				  		<Col sm="2">
					</Col>

					</Row>

					<Row>
						<Col xs="4" sm="2" ></Col>
						<Col xs="8" sm="8" >

								<h3>Melody with Harmonizing Layer</h3>
								<HarmonyRoll/>
								<p>
								  <Button color="primary">Download</Button>
								</p>

						</Col>
						<Col sm="2"></Col>
					</Row>

					<Row>
						<Col xs="4" sm="2" ></Col>
						<Col xs="8" sm="8" >

								<h3>Melody with Harmonizing Layer and Drums</h3>
								<DrumRoll/>
								<p>
								  <Button color="primary">Download</Button>
								</p>

						</Col>
						<Col sm="2"></Col>
					</Row>
				</div>
				<Footer/>
			</div>
		)
	}
}

export default Project
