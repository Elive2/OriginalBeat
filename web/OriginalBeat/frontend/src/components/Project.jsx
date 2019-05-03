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
		console.log(innerDoc1.server);
		console.log("innerdoc1");
		var iframe = document.getElementById('harmony');
		var innerDoc2 = iframe.contentDocument || iframe.contentWindow.document;
		var iframe = document.getElementById('drum');
		var innerDoc3 = iframe.contentDocument || iframe.contentWindow.document;

        innerDoc1.getElementById('PlayPause').click();
		innerDoc2.getElementById('PlayPause').click();
		innerDoc3.getElementById('PlayPause').click();

     }
	 reSync(){
		 window.location.reload();
	 }

	render() {
		return (
			<div>
				<Header/>
				<div class = "title">
					<Row>
						<Col>

								<Button color="secondary" onClick={this.playAll}>Play All</Button>
								<Button color="secondary" onClick={this.reSync}>Re-Sync</Button>

						</Col>
					</Row>

					<Row>
						<Col xs="4" sm="2" >
							<h3 Style="font-size: 30px;">Original Melody</h3>
						</Col>
				    	<Col xs="8" sm="8" >



								<MelodyRoll/>

						</Col>

				  		<Col sm="2">
							<Form method="get" action="/download/">
								<Button type="submit" color="primary">Download</Button>
							</Form>
						</Col>

					</Row>

					<Row>
						<Col xs="4" sm="2" >
							<h3 Style="font-size: 30px;">Harmony Layer</h3>
						</Col>
						<Col xs="8" sm="8" >


								<HarmonyRoll/>


						</Col>
						<Col sm="2">
							<p>
							  <Button color="primary">Download</Button>
							</p>
						</Col>
					</Row>

					<Row>
						<Col xs="4" sm="2" >
							<h3 Style="font-size: 30px;">Drums Layer</h3>
						</Col>
						<Col xs="8" sm="8" >


								<DrumRoll/>

						</Col>
						<Col sm="2">
							<p>
							  <Button color="primary">Download</Button>
							</p>
						</Col>
					</Row>
				</div>
				<Footer/>
			</div>
		)
	}
}

export default Project
