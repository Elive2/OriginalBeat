import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';



class Contact extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Header pageSelected={'Contact'}/>
					<Row>
						<div class = "title">
							<Row>
								<Col>
								<h3 class = "font-effect-anaglyp"> Contact Us </h3>

								</Col>
							</Row>
							<Row>
								<Col >
									<Jumbotron className="contact">
										<Row>
											<Col>
												<h5>Eli Yale</h5>
											</Col>
											<Col>
												<Row>
													<p style={{ marginRight: 10 }}>email:  </p> <a href={"mailto:" + "eyale@scu.edu"}>eyale@scu.edu</a>
												</Row>
											</Col>
										</Row>

										<Row>
											<Col>
												<h5>Christian Quintero</h5>
											</Col>
											<Col>
												<Row>
													<p style={{ marginRight: 10 }}>email:  </p> <a href={"mailto:" + "cquintero@scu.edu"}>cquintero@scu.edu</a>
												</Row>
											</Col>
										</Row>

										<Row>
											<Col>
												<h5> Matt Kordonsky </h5>
											</Col>
											<Col>
												<Row>
													<p style={{ marginRight: 10 }}>email:  </p> <a href={"mailto:" + "mkordonsky@scu.edu"}>mkordonsky@scu.edu</a>
												</Row>
											</Col>
										</Row>
									</Jumbotron>
								</Col>
							</Row>
						</div>
					</Row>
				<Footer/>
			</div>
		)
	}
}

export default Contact
