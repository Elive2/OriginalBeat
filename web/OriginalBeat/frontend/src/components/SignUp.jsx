import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Footer from './Footer';
import CSRFToken from './CSRFToken';

var server = process.env.API_URL + "midi/";


class SignUp extends React.Component{
	constructor(props) {
	  super(props);
	}

	render() {
		return (
			<div className="login">
				<Row>
					<Col sm="12" md={{ size: 6, offset: 3 }}>
						<Jumbotron className="loginForm">
							<h2>Sign Up</h2>
							<Form encType="multipart/form-data" action='/accounts/signup/' method="post">
							<CSRFToken />
							<Row>
								<Col>
									<FormGroup>
										<p>
											<Label for="id_username">Username</Label>
											<Input type="text" name="username" maxlength="150" autofocus required id="id_username"/>
											<span class="helptext">Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.</span>
										</p>
										<p>
											<Label for="id_password1">Password</Label>
											<Input type="password" name="password1" required id="id_password1"/>
											<span class="helptext">
												<ul>
													<li>Your password can&#39;t be too similar to your other personal information.</li>
													<li>Your password must contain at least 8 characters.</li>
													<li>Your password can&#39;t be a commonly used password.</li>
													<li>Your password can&#39;t be entirely numeric.</li>
												</ul>
											</span>
										</p>
										<p>
											<Label for="id_password2">Password confirmation:</Label> 
											<Input type="password" name="password2" required id="id_password2"/>
											<span class="helptext">Enter the same password as before, for verification.</span>
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
						</Jumbotron>
					</Col>
				</Row>
				<Footer/>
			</div>
		)
	}
}

export default SignUp
