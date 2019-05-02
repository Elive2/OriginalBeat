import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';

class DrumRoll extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Row>
					<Col>
						<iframe id = "drum" src={'/static/pianoRoll.html'} height="300" width="100%"></iframe>
					</Col>
				</Row>
			</div>

		)
	}
}

export default DrumRoll
