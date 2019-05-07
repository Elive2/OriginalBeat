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

	pageSelected = [''];
	state = {
		pageSelected: this.props.pageSelected
	};

	thisPage () {
		if (this.props.pageSelected == this.getElementById('About'))
			return ('active')
		else
			return ('')
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
						<a href='/'>
							<img className="logo" src={"/static/logo.png"}/>
						</a>
					</Col>
					<Col>
						<div  className="topnav">
						  <a id='Home' className= {this.thisPage} href="/">Home</a>
						  <a id='About' className= {this.thisPage} href="/about">About</a>
						  <a id='Profile' className= {this.thisPage} href="/accounts/login">Profile</a>
						  <a id='Contact' className= {this.thisPage} href="/contact.html">Contact</a>
						</div>
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
			</header>
		)
	}
}

export default Header
