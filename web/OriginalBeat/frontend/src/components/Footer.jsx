import React from 'react';
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
					<Col sm="12" md={{ size: 6, offset: 3 }}>
						<a href="https://github.com/Elive2/OriginalBeat"><img className="github" src={"/static/GitHub-Mark-64px.png"}/></a>
					</Col>
				</Row>
			</footer>
		)
	}
}

export default Footer