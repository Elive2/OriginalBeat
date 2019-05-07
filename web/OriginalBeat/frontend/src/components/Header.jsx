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

	checkClass(name){
		if (this.props.pageSelected == name)
			return ("active")
		else {
			return ("nonactive")
		}
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
						  <a className={this.checkClass('Home')}  href="/">Home</a>
						  <a className={this.checkClass('About')}  href="/about">About</a>
						  <a className={this.checkClass('Profile')}  href="/accounts/login">Profile</a>
						  <a className={this.checkClass('Contact')}  href="/contact">Contact</a>
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
