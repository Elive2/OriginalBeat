import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';


class MelodyRoll extends React.Component{
	constructor(props) {
	  super(props);
	}

	setUpFrame() {
		var frame = window.frames['melody'];
		frame.setMidiPath('../data/output/output_melody.mid');
	}

	render() {


		return (
			<div>
				<Row>
					<Col>
						<div className="pianorollFrame">

							<body>
								<iframe name = "melody" id = "melody" src={'/static/pianoRoll.html'} scrolling="no" height="300" width="100%" ></iframe>
							</body>
						</div>
					</Col>
				</Row>
			</div>

		)
	}
}

export default MelodyRoll
