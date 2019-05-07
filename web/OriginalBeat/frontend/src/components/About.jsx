import React from 'react';
import '../index.css';
import { Container, Row, Col, Form, FormGroup, Label, Input, FormText, Jumbotron, Button} from 'reactstrap';
import Header from './Header';
import Footer from './Footer';



class About extends React.Component{
	constructor(props) {
	  super(props);
	}
	render() {
		return (
			<div>
				<Header pageSelected={'About'}/>
					<Row>
						<div class = "title">
							<Row>
								<Col>
								<a href='/'>
									<img className="bigLogo" src={"/static/logo.png"}/>
								</a>
								</Col>
							</Row>
							<Row>
								<Col>
								<h3 class = "font-effect-anaglyp"> About Us </h3>

								</Col>
							</Row>
							<Row>
								<Col className = "aboutCol">
									<Jumbotron>
										<p className="aboutBio"><p>
										The barrier to entry in electronic music production  is high. It requires expensive, complicated software and extensive knowledge of music theory and experience with sound generation. These Digital Audio Workstations are great for professionals but they have a steep learning curve for beginners who just want to begin making tracks for simple songs they may have in their heads.
										Electronic music including EDM and Progressive house is a genre of music where a majority of songs consist of layer of digital sounds generated by a computer. It is up to the producer to arrange the drum sounds into a rhythm, then select synthesizer notes to create a melody. Many producers add additional digital sounds to complement the melody and rhythm and add to the complexity of the track. The layered nature of electronic music means there is lots of room for computer generation in the production process. <br /></p><p>
										This is where our app aims to fill the gaps. Rather than requiring a user to generate every layer in their song, we will enable them to start with one layer, and our system will generate the other layers and sounds. For example if a user has a simple melody in their head, they may upload it in MIDI format to our system, and our system will work to generate an accompanying harmony and drumline.
										</p></p>
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

export default About
