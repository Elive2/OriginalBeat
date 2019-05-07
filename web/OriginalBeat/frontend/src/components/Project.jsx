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

let instrument = ['synth', 'piano'];



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
	 reSync(){
		document.getElementById('melody').src = document.getElementById('melody').src
		document.getElementById('harmony').src = document.getElementById('harmony').src
		document.getElementById('drum').src = document.getElementById('drum').src

	 }


	render() {
		return (
			<div>
				<Header/>
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



								<MelodyRoll/>

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


								<HarmonyRoll/>


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


								<DrumRoll/>

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
