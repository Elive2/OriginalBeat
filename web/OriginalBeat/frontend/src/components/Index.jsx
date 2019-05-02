import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import CSRFToken from './CSRFToken';


class Index extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Header/>
					<div class = "title">

						<Row>
			
							<h3>Welcome to the </h3>
						</Row>
						<Row>
							<h4>Original Beat!</h4>
						</Row>
						<Row>
							<h2> To begin please select an option below</h2>
						</Row>
						<Row>
							<Col xs="6"> <Button color="primary">Create Melody</Button> </Col>
	  						<Col xs="6"><Button color="primary">Upload Melody</Button></Col>
						</Row>
					</div>
				<Footer/>
			</div>
		)
	}
}

export default Index
