import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';
import CSRFToken from './CSRFToken';

var server = "http://127.0.0.1:8000/midi/";


class Index extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Header/>
					<h1>Welcome to the Original Beat!</h1>
				<Footer/>
			</div>
		)
	}
}

export default Index
