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
				<Header pageSelected={'Home'}/>
					<div class = "title">

						<Row>
							<Col>
							<h3>Welcome to the </h3>
							</Col>
						</Row>
						<Row>
							<Col>
								<img src={'/static/logo-lg.png'} id="logo-lg"/>
							</Col>
						</Row>
						<Row>
							<Col sm="12" md={{ size: 6, offset: 3 }}>
								<Jumbotron>
									<Row>
										<Col>
										<h3 Style="font-size: 25px;"> To begin please sign in</h3>
										</Col>
									</Row>
									<Row>
										<Col>
											<Form method="get" action="/accounts/login">
												<Button color="secondary">Sign In</Button>
											</Form>
										</Col>
									</Row>
								</Jumbotron>
							</Col>
						</Row>
					</div>
				<Footer/>
			</div>
		)
	}
}

export default Index
