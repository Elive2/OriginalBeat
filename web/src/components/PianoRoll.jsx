import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';

class PianoRoll extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<iframe src='./pianoRoll.html' height="400" width="100%"></iframe>
			</div>
		)
	}
}

export default PianoRoll