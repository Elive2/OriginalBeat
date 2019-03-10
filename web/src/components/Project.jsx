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
					<Row>
						<Col>
								<PianoRoll/>
						</Col>
					</Row>
				<Footer/>
			</div>
		)
	}
}

export default Project
