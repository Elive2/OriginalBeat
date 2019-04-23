import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import PianoRoll from './PianoRoll'

class Project extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Header/>
				<div class = "title">
					<Row>
						<Col xs="4" sm="2" ></Col>
				    	<Col xs="8" sm="8" >

								<h3>Original Melody</h3>
								<PianoRoll/>
								<p>
						          <Button color="primary">Download</Button>
						        </p>

						</Col>
				  		<Col sm="2"></Col>

					</Row>
					<Row>

					</Row>
				</div>
				<Footer/>
			</div>
		)
	}
}

export default Project
