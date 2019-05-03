import React from 'react';
import '../index.css';
import { Container, Row, Col, Dropdown, DropdownToggle, DropdownMenu, DropdownItem,Collapse,
	  Navbar,
	  NavbarToggler,
	  NavbarBrand,
	  Nav,
	  NavItem,
	  NavLink,
	  UncontrolledDropdown} from 'reactstrap';

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
						<h4 className="name">Original<br/>Beat </h4>
					</Col>
					<Col>
						<Dropdown isOpen={this.state.dropdownOpen} toggle={this.toggle} id="profile">
			        <DropdownToggle caret>
			          Profile
			        </DropdownToggle>
			        <DropdownMenu>
			          <DropdownItem><a href="/accounts/logout">Log Out</a></DropdownItem>
			        </DropdownMenu>
      			</Dropdown>
					</Col>
				</Row>
				<Row>
				<div class="topnav">
				  <a class="active" href="/">Home</a>
				  <a href="/templates/OriginalBeat/about.html">About</a>
				  <a href="/accounts/login">Profile</a>
				  <a href="/templates/OriginalBeat/contact.html">Contact</a>
				</div>

				</Row>
			</header>
		)
	}
}

export default Header
