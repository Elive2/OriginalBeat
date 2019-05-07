import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';

class HarmonyRoll extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Row>
					<Col>
						<div className="pianorollFrame">
							<iframe id = "harmony" src={'/static/pianoRoll.html'} scrolling="no" height="300" width="100%"></iframe>
						</div>
					</Col>
				</Row>
			</div>

		)
	}
}

export default HarmonyRoll
