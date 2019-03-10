import React from 'react';
import logo from './logo.png';
import '../index.css';
import { Container, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem} from 'reactstrap';

class Footer extends React.Component{
	constructor(props) {
	  super(props);
	}

	render() {
		return (
			<footer>
				<Row>
					<Col>
						<img className="logo" src={logo}/>
						<h2 className="name">Original<br/>Beat </h2>
					</Col>
				</Row>
			</footer>
		)
	}
}

export default Footer