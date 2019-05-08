import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';


class MelodyRoll extends React.Component{
	constructor(props) {
	  super(props);
	}

	inst = [''];
	state = {	inst: this.props.inst
				} ;

	setUpFrame() {
		var frame = window.frames['melody'];
		frame.setMidi(this.props.midi);
	}

	getID(){
		return this.props.inst;
	}

	render() {


		return (
			<div>
				<Row>
					<Col>
						<div className="pianorollFrame">

							<body>
								<iframe id = {this.props.inst} src={'/static/pianoRoll.html'} scrolling="no" height="300" width="100%" ></iframe>
							</body>
						</div>
					</Col>
				</Row>
			</div>

		)
	}
}

export default MelodyRoll
