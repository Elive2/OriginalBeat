import React from 'react';
import '../index.css';
import { Container, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem} from 'reactstrap';

class Header extends React.Component{
	constructor(props) {
	  super(props);

	  this.toggle = this.toggle.bind(this);
	  this.state = {
	    dropdownOpen: false
	  };
	}

	toggle() {
	  this.setState({
	    dropdownOpen: !this.state.dropdownOpen
	  });
	}
	render() {
		return (
			<header>
				<Row>
					<Col>
						<img className="logo" src={"/static/logo.png"}/>
						<h2 className="name">Original<br/>Beat </h2>
					</Col>
					<Col xs="6">
						<Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle} id="profile">
			        <DropdownToggle caret>
			          Profile
			        </DropdownToggle>
			        <DropdownMenu>
			          <DropdownItem><a href="logout.php">Log Out</a></DropdownItem>
			        </DropdownMenu>
      			</Dropdown>
					</Col>
				</Row>
			</header>
		)
	}
}

export default Header
