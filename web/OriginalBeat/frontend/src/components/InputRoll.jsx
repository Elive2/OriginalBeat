import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';



class InputRoll extends React.Component{
	constructor(props) {
	  super(props);
	}


	componentDidMount(){
		this.ifr.onload = () => {
			//console.log("IFRAME LOADES")
			//this.ifr.contentWindow.postMessage('hello', "*");
			//console.log(this.props.midi)
			this.sendToFrame(JSON.parse(JSON.stringify(this.props.midi)));
		}
		//window.addEventListener("message", this.handleFrameTasks);

	}

	componentWillUpdate() {
		console.log("COMPONENT WILL UPDATE")
		this.sendToFrame(JSON.parse(JSON.stringify(this.props.midi)));

	}

	sendToFrame(data) {
    if(this.ifr) this.ifr.contentWindow.postMessage(data, '*');
  }

	inst = [''];
	state = {	inst: this.props.inst
				
	};

	getID(){
		return this.props.inst;
	}

	render() {
		console.log("INPUT ROLL RERENDERING")


		return (
			<div>
				<Row>
					<Col>
						<div className="inputRollFrame">
							<iframe 
								name = "melody" 
								id = {this.props.inst} 
								src={'/static/pianoRoll.html'} 
								scrolling="no" 
								height="300" 
								width="100%"
								ref={(f) => {this.ifr = f;} }
							/>
						</div>
					</Col>
				</Row>
			</div>

		)
	}
}

export default InputRoll
