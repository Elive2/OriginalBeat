import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Footer from './Footer';
import CSRFToken from './CSRFToken';

var server = process.env.API_URL + "midi/";


class Login extends React.Component{
	constructor(props) {
	  super(props);
	}

	render() {
		return (
			<div className="login">
				<Row>
					<Col sm="12" md={{ size: 4, offset: 4 }}>
						<Jumbotron className="loginForm">
							<h1>Welcome!</h1>
							<h2>Sign In</h2>
							<Form encType="multipart/form-data" action='/accounts/login/' method="post">
							<CSRFToken />
							<Row>
								<Col>
									<FormGroup>
										<p>
											<Label for="id_username">Username</Label>
											<Input type="text" name="username" autofocus required id="id_username"/>
										</p>
										<p>
											<Label for="id_password">Password</Label>
											<Input type="password" name="password" required id="id_password"/>
										</p>
									</FormGroup>
								</Col>
							</Row>
							<Row>
								<Col>
									<Button type="submit">Login</Button>
								</Col>
							</Row>
							</Form>
							<Row>
								<Col>
									Don't have an account?
								</Col>
							</Row>
							<Row>
								<Col>
									<a href='/accounts/signup/'>Sign Up</a>
								</Col>
							</Row>
						</Jumbotron>
					</Col>
				</Row>
				<Footer/>
			</div>
		)
	}
}
export default Login
